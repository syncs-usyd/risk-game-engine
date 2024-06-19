from typing import Union, TYPE_CHECKING
from engine.config.gameconfig import NUM_PLAYERS, NUM_STARTING_TROOPS
from engine.game.card import Card
from engine.game.map import Map
from engine.game.player import Player
from engine.game.territory import Territory
from engine.maps import earth

if TYPE_CHECKING:
    from engine.records.moves.move_attack import MoveAttack
    from engine.records.moves.move_claim_territory import MoveClaimTerritory
    from engine.records.moves.move_defend import MoveDefend
    from engine.records.moves.move_fortify import MoveFortify
    from engine.records.moves.move_place_initial_troop import MovePlaceInitialTroop
    from engine.records.moves.move_redeem_cards import MoveRedeemCards
    from engine.records.record_attack import RecordAttack
    from engine.records.record_drew_card import RecordDrewCard
    from engine.records.record_player_eliminated import RecordPlayerEliminated
    from engine.records.record_redeemed_cards import RecordRedeemedCards
    from engine.records.record_shuffled_cards import RecordShuffledCards
    from engine.records.record_start_turn import RecordStartTurn
    from engine.records.record_territory_conquered import RecordTerritoryConquered
    from engine.records.record_start_game import RecordStartGame

class State():
    def __init__(self):
        self.map: Map = earth.create_map()
        self.cards: dict[int, Card] = earth.create_cards() 
        self.deck: list[Card] = list(self.cards.values())
        self.discarded_deck: list[Card] = []
        self.players: dict[int, Player] = dict([(x, Player.factory(player_id=x, initial_troops=NUM_STARTING_TROOPS)) for x in range(NUM_PLAYERS)])
        self.territories: dict[int, Territory] = dict([(x, Territory(territory_id=x, occupier=None, troops=0)) for x in self.map.get_vertices()])
        self.card_sets_redeemed: int = 0
        self.turn_order: list[int] = [x.player_id for x in self.players.values()]
        self.match_history: list[Union['RecordAttack', 'RecordDrewCard', 'RecordPlayerEliminated',
                            'RecordRedeemedCards', 'RecordShuffledCards', 'RecordStartGame', 
                            'RecordStartTurn', 'RecordTerritoryConquered', 'MoveAttack', 
                            'MoveClaimTerritory', 'MoveDefend', 'MoveFortify', 
                            'MovePlaceInitialTroop', 'MoveRedeemCards']] = []
                            