import random
import shutil
from typing import Tuple
from collections import deque

from engine.config.ioconfig import CORE_DIRECTORY
from engine.connection.player_connection import PlayerConnection
from engine.exceptions import PlayerException
from engine.game.player import Player
from engine.game.state import State
from engine.output.game_result import GameBanResult, GameSuccessResult
from engine.output.recording_inspector import RecordingInspector
from engine.records.record_attack import RecordAttack
from engine.records.record_banned import RecordBanned
from engine.records.record_player_eliminated import RecordPlayerEliminated
from engine.records.record_shuffled_cards import RecordShuffledCards
from engine.records.record_start_game import RecordStartGame
from engine.records.record_start_turn import RecordStartTurn
from engine.records.record_territory_conquered import RecordTerritoryConquered
from engine.records.record_winner import RecordWinner

def get_next_turn(state: State, connections: dict[int, PlayerConnection], turn_order: deque[int]) -> Tuple[Player, PlayerConnection]:
        player_id = turn_order.pop()
        turn_order.appendleft(player_id)
        player = state.players[player_id]
        connection = connections[player_id]

        return (player, connection)


class GameEngine:
    def __init__(self):
        self.state = State()
        self.connections = dict([(x, PlayerConnection(player_id=x)) for x in self.state.players.keys()])


    def start(self):
        try:
            self._run_game()
        except PlayerException as e:
            record = RecordBanned.factory(e)
            record.commit(self.state)

        self._finish()


    def _finish(self):

        # Write the result.
        inspector = RecordingInspector(self.state.recording)
        result = inspector.get_result()

        with open(f"{CORE_DIRECTORY}/output/results.json", "w") as f:
            f.write(result.model_dump_json())

        # Write the game log.
        with open(f"{CORE_DIRECTORY}/output/game.log", "w") as f:
            f.write(inspector.get_recording_json())

        def copy_stdout_stderr_player(player: int):
            stderr_path = f"{CORE_DIRECTORY}/submission{player}/io/submission.err"
            stderr_path_new = f"{CORE_DIRECTORY}/output/submission_{player}.err"
            stdout_path = f"{CORE_DIRECTORY}/submission{player}/io/submission.log"
            stdout_path_new = f"{CORE_DIRECTORY}/output/submission_{player}.log"

            try:
                shutil.copy(stderr_path, stderr_path_new, follow_symlinks=False)
            except (FileNotFoundError, IsADirectoryError, FileExistsError):
                with open(stderr_path_new, "w") as f:
                    f.write("Your submission.err file is either missing or is a directory.")
            
            try:
                shutil.copy(stdout_path, stdout_path_new, follow_symlinks=False)
            except (FileNotFoundError, IsADirectoryError, FileExistsError):
                with open(stdout_path_new, "w") as f:
                    f.write("Your submission.log file is either missing or is a directory.")


        # Only copy for the player who was banned, otherwise copy for all players.
        match result:
            case GameBanResult() as x:
                copy_stdout_stderr_player(player=x.player)

            case GameSuccessResult():
                for player in self.state.players.keys():
                    copy_stdout_stderr_player(player)


    def _run_game(self):
        
        # Emit RecordStartGame.
        turn_order = list(self.state.players.keys())
        random.shuffle(turn_order)
        record_start_game = RecordStartGame(turn_order=self.state.turn_order.copy(), players=[Player.model_validate(v.model_dump()).get_public() for v in self.state.players.values()])
        record_start_game.commit(self.state)

        # Emit RecordShuffledCards.
        record_shuffled_cards = RecordShuffledCards()
        record_shuffled_cards.commit(self.state)

        # Run the initial phases.
        self._start_claim_territories_phase()
        self._start_place_initial_troops_phase()

        # Run the main game.
        turn_order = deque(self.state.turn_order.copy())
        while len(list(filter(lambda x: x.alive == True, self.state.players.values()))) > 1:
            
            player, connection = get_next_turn(self.state, self.connections, turn_order)
            if not player.alive: continue

            self._troop_phase(player, connection)
            self._attack_phase(player, connection)
            self._fortify_phase(player, connection)

        # Emit RecordWinner.
        winner = filter(lambda x: x.alive == True, self.state.players.values()).__next__().player_id
        record = RecordWinner(player=winner)
        record.commit(self.state)



    def _start_claim_territories_phase(self):
        turn_order = deque(self.state.turn_order.copy())

        while len(list(filter(lambda x: x.occupier == None, self.state.territories.values()))) > 0:
            _, connection = get_next_turn(self.state, self.connections, turn_order)
            response = connection.query_claim_territory(self.state)
            response.commit(self.state)


    def _start_place_initial_troops_phase(self):
        turn_order = deque(self.state.turn_order.copy())

        while len(list(filter(lambda x: x.troops_remaining > 0, self.state.players.values()))) > 0:
            player, connection = get_next_turn(self.state, self.connections, turn_order)

            if player.troops_remaining == 0:
                continue

            response = connection.query_place_initial_troop(self.state)
            response.commit(self.state)


    def _troop_phase(self, player: Player, connection: PlayerConnection):
        
        # Emit a RecordStartTurn.
        record = RecordStartTurn.factory(self.state, player.player_id)
        record.commit(self.state)

        # Let the player redeem cards.
        response = connection.query_redeem_cards(self.state, cause="turn_started")
        response.commit(self.state)

        # Let the player distribute troops.
        response = connection.query_distribute_troops(self.state, cause="turn_started")
        response.commit(self.state)


    def _attack_phase(self, player: Player, connection: PlayerConnection):

        while (True):

            # Get the attack move.
            attack = connection.query_attack(self.state)
            attack.commit(self.state)
            move_attack_id = len(self.state.recording) - 1

            # If the player passes, move to the next phase.
            if attack.move == "pass":
                break
            
            defending_player = self.state.territories[attack.move.defending_territory].occupier
            if defending_player == None:
                raise RuntimeError("Tried to attack unoccupied territory.")

            # Get the defend move.
            defend = self.connections[defending_player].query_defend(self.state, move_attack_id)
            defend.commit(self.state)
            move_defend_id = len(self.state.recording) - 1

            # Emit the RecordAttack.
            record_attack = RecordAttack.factory(state=self.state, move_attack_id=move_attack_id, move_defend_id=move_defend_id)
            record_attack.commit(self.state)
            record_attack_id = len(self.state.recording) - 1

            # Emit a RecordTerritoryConquered and then allow player to move troops.
            if record_attack.territory_conquered:
                record = RecordTerritoryConquered(record_attack_id=record_attack_id)
                record.commit(self.state)

                response = connection.query_troops_after_attack(self.state, record_attack_id)
                response.commit(self.state)

            # Emit a RecordPlayerEliminated and then allow player to redeem cards and distribute troops if required.
            if record_attack.defender_eliminated:
                record = RecordPlayerEliminated.factory(self.state, move_defend_id, defending_player)
                record.commit(self.state)

                if len(player.cards) > 6:
                    response = connection.query_redeem_cards(self.state, cause="player_eliminated")
                    response.commit(self.state)

                    response = connection.query_distribute_troops(self.state, cause="player_eliminated")
                    response.commit(self.state)


    def _fortify_phase(self, player: Player, connection: PlayerConnection):
        response = connection.query_fortify(self.state)
        response.commit(self.state)
        