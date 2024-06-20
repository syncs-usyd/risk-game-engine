import random
from typing import Tuple
from collections import deque

from engine.connection.player_connection import PlayerConnection
from engine.exceptions import EngineException
from engine.game.player import Player
from engine.game.state import State
from engine.records.record_attack import RecordAttack
from engine.records.record_player_eliminated import RecordPlayerEliminated
from engine.records.record_shuffled_cards import RecordShuffledCards
from engine.records.record_start_game import RecordStartGame
from engine.records.record_start_turn import RecordStartTurn
from engine.records.record_territory_conquered import RecordTerritoryConquered

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

        turn_order = list(self.state.players.keys())
        random.shuffle(turn_order)
        self.turn_order = deque(turn_order)


    def start(self):
        try:
            self._run_game()
        except EngineException as e:
            # Terminate with a result.json blaming the faulty player.
            pass


    def _start_claim_territories_phase(self):
        turn_order = self.turn_order.copy()

        while len(list(filter(lambda x: x.occupier == None, self.state.territories.values()))) > 0:
            _, connection = get_next_turn(self.state, self.connections, turn_order)
            response = connection.query_claim_territory(self.state)
            response.commit(self.state)


    def _start_place_initial_troops_phase(self):
        turn_order = self.turn_order.copy()

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
            move_attack_id = len(self.state.match_history) - 1

            # If the player passes, move to the next phase.
            if attack.move == "pass":
                break
            
            defending_player = self.state.territories[attack.move.defending_territory].occupier
            if defending_player == None:
                raise RuntimeError("Tried to attack unoccupied territory.")

            # Get the defend move.
            defend = self.connections[defending_player].query_defend(self.state, move_attack_id)
            defend.commit(self.state)
            move_defend_id = len(self.state.match_history) - 1

            # Emit the RecordAttack.
            record_attack = RecordAttack.factory(state=self.state, move_attack_id=move_attack_id, move_defend_id=move_defend_id)
            record_attack.commit(self.state)
            record_attack_id = len(self.state.match_history) - 1

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


    def _run_game(self):

        # Emit RecordStartGame and RecordShuffledCards.
        record_start_game = RecordStartGame(turn_order=self.state.turn_order.copy(), players=[Player.model_validate(v.model_dump()).get_public() for v in self.state.players.values()])
        record_start_game.commit(self.state)

        record_shuffled_cards = RecordShuffledCards()
        record_shuffled_cards.commit(self.state)

        self._start_claim_territories_phase()
        self._start_place_initial_troops_phase()

        turn_order = self.turn_order.copy()
        while len(list(filter(lambda x: x.alive == True, self.state.players.values()))) > 1:
            
            player, connection = get_next_turn(self.state, self.connections, turn_order)
            if not player.alive: continue

            self._troop_phase(player, connection)
            self._attack_phase(player, connection)
            self._fortify_phase(player, connection)

        # Emit RecordWinner.
        winner = filter(lambda x: x.alive == True, self.state.players.values()).__next__().player_id
        
        
        # Terminate successfully.

        