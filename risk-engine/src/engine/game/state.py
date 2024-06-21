from engine.config.gameconfig import NUM_PLAYERS, NUM_STARTING_TROOPS
from engine.game.card import Card
from engine.game.map import Map
from engine.game.player import Player
from engine.game.state_mutator import StateMutator
from engine.game.territory import Territory
from engine.maps import earth
from engine.records.types.record_type import RecordType

class State():
    def __init__(self):
        self.map: Map = earth.create_map()
        self.cards: dict[int, Card] = earth.create_cards() 
        self.deck: list[Card] = []
        self.discarded_deck: list[Card] = list(self.cards.values())
        self.players: dict[int, Player] = dict([(x, Player.factory(player_id=x, initial_troops=NUM_STARTING_TROOPS)) for x in range(NUM_PLAYERS)])
        self.territories: dict[int, Territory] = dict([(x, Territory(territory_id=x, occupier=None, troops=0)) for x in self.map.get_vertices()])
        self.card_sets_redeemed: int = 0
        self.turn_order: list[int] = [x.player_id for x in self.players.values()]
        self.recording: list[RecordType] = []
        self.mutator = StateMutator(self)
    

    def commit(self, record: RecordType) -> None:
        self.recording.append(record)
        self.mutator.commit(record)