from engine.config.gameconfig import NUM_PLAYERS, NUM_STARTING_TROOPS
from engine.game.card import Card
from engine.game.map import Map
from engine.game.player import Player
from engine.game.territory import Territory
from engine.maps import earth
from engine.models.card_model import CardModel
from engine.records.base_record import BaseRecord

class State():
    def __init__(self):
        self.map: Map = earth.create_map()
        self.cards: dict[int, Card] = earth.create_cards() 
        self.deck: list[Card] = list(self.cards.values())
        self.players: dict[int, Player] = dict([(x, Player.factory(player_id=x, initial_troops=NUM_STARTING_TROOPS)) for x in range(NUM_PLAYERS)])
        self.territories: dict[int, Territory] = dict([(x, Territory(territory_id=x, occupier=None, troops=0)) for x in self.map.get_vertices()])
        self.match_history: list[BaseRecord] = []
        self.card_sets_redeemed: int = 0

    def _apply_record(self, record: BaseRecord):

        pass