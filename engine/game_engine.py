import random
from typing import Tuple
from engine.config.gameconfig import NUM_PLAYERS
from collections import deque

from engine.connection.player_connection import PlayerConnection
from engine.exceptions import EngineException
from engine.game.player import Player
from engine.game.state import State

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

        # TODO: Add game log.


    def start(self):
        try:
            self._run_game()
        except EngineException as e:
            # Terminate with a result.json blaming the faulty player.
            pass


    def _start_claim_territories_phase(self):
        turn_order = self.turn_order.copy()

        while len(list(filter(lambda x: x.occupier == None, self.state.territories.values()))) > 0:
            player, connection = get_next_turn(self.state, self.connections, turn_order)
            response = connection.query_claim_territory(self.state)

            # The player claims this territory and places one troop there.
            claimed_territory = self.state.territories[response.territory_id]
            claimed_territory.occupier = player.player_id
            claimed_territory.troops = 1
            player.troops -= 1


    def _start_place_initial_troops_phase(self):
        turn_order = self.turn_order.copy()

        while len(list(filter(lambda x: x.troops > 0, self.state.players.values()))) > 0:
            player, connection = get_next_turn(self.state, self.connections, turn_order)

            if player.troops == 0:
                continue

            response = connection.query_place_initial_troop(self.state)

            # The player increases the troop count of this territory by one.
            selected_territory = self.state.territories[response.territory_id]
            selected_territory.troops += 1
            player.troops -= 1

    def _player_troop_phase(self, player: Player, connection: PlayerConnection):
        # Player can redeem cards.
        if len(list(player.get_cards())) > 5:
            response_cards = connection.query_redeem_player_cards(self.state)
        else:
            response_decision = connection.query_redeem_card_decision(self.state)
            if response_decision:
                response_cards = connection.query_redeem_player_cards(self.state)
                # Redeem cards. TODO: Write the code for this later. gaming break
                # player.troops = add bonus troops from redeemed cards.
                # remove cards from player
                # add cards to deck

        
        # Calculating player's troop count with territories and continents.
        player_territories = [territory_id for territory_id, territory in self.state.territories.items() if territory.occupier == player.player_id]
        player.troops += max(3, len(player_territories) // 3)

        # Since I have changed alot of stuff check if this for loop still works later
        for continent, territories in self.state.map._continents.items():
            if all(territory_id in player_territories for territory_id in territories.values()): # type: ignore
                player.troops += self.state.map._continent_bonuses[continent]

        # Player can place troops on territories they own.
        while player.troops != 0:
            response = connection.query_place_player_troop(self.state)

            # The player increases the troop count of this territory depending on how many troops they want to place.
            selected_territory = self.state.territories[response.territory_id]
            selected_territory.troops += 1
            player.troops -= 1

    def _run_game(self):

        self._start_claim_territories_phase()
        self._start_place_initial_troops_phase()

        print(f"Starting game...")

        # Main game loop phase.
        turn_order = self.turn_order.copy()
        while len(list(filter(lambda x: x.alive == True, self.state.players.values()))) > 1:
            
            player, connection = get_next_turn(self.state, self.connections, turn_order)
            # Troop phase.
            # ...

            # Attack phase.
            # ...

            # Fortification phase.
            # ...

        # Game ended.
        winner = filter(lambda x: x.alive == True, self.state.players.values()).__next__().player_id

        # Terminate successfully.

        