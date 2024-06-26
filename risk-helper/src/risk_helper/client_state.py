from collections import defaultdict
from typing import Optional, Tuple, Union
from risk_shared.maps import earth
from risk_shared.models.card_model import CardModel
from risk_shared.models.player_model import PlayerModel, PublicPlayerModel
from risk_shared.models.territory_model import TerritoryModel
from risk_shared.records.types.record_type import RecordType


class ClientState():

    def __init__(self):
        self.map = earth.create_map()
        self.cards = earth.create_cards()
        self.deck_card_count: int = 0
        self.discarded_deck: list[CardModel] = list(self.cards.values())
        self.players: dict[int, PublicPlayerModel] = {}
        self.territories: dict[int, TerritoryModel] = dict([(x, TerritoryModel(territory_id=x, occupier=None, troops=0)) for x in self.map.get_vertices()])
        self.card_sets_redeemed: int = 0
        self.turn_order: list[int] = []
        self.recording: list[RecordType] = []
        self.new_records: int = 0
        self.me: PlayerModel


    def get_card_set(self, cards: list[CardModel]) -> Optional[Tuple[CardModel, CardModel, CardModel]]:
        cards_by_symbol: dict[str, list[CardModel]] = defaultdict(list)
        for card in cards:
            cards_by_symbol[card.symbol].append(card)
        
        # Try to make a different symbols set.
        symbols_held = [symbol for symbol in cards_by_symbol.keys() if len(cards_by_symbol[symbol]) > 0]
        if len(symbols_held) >= 3:
            return (cards_by_symbol[symbols_held[0]][0], cards_by_symbol[symbols_held[1]][0], cards_by_symbol[symbols_held[2]][0])
        
        # To prevent implicitly modifying the dictionary in the for loop, we explicitly initialise the "Wildcard" key.
        cards_by_symbol["Wildcard"]
        
        # Try to make a matching symbols set.
        for symbol, _cards in cards_by_symbol.items():
            if symbol == "Wildcard":
                continue

            if len(_cards) >= 3:
                return (_cards[0], _cards[1], _cards[2])
            elif len(_cards) == 2 and len(cards_by_symbol["Wildcard"]) >= 1:
                return (_cards[0], _cards[1], cards_by_symbol["Wildcard"][0])
            elif len(_cards) == 1 and len(cards_by_symbol["Wildcard"]) >= 2:
                return (_cards[0], cards_by_symbol["Wildcard"][0], cards_by_symbol["Wildcard"][1])


    def get_territories_owned_by(self, player: Union[int, None]) -> list[int]:
        return list([y.territory_id for y in filter(lambda x: x.occupier == player, self.territories.values())])
    
    
    def get_all_border_territories(self, territories: list) -> list[int]:
        return [territory for territory in territories if len(set(self.map.get_adjacent_to(territory)) - set(territories)) != 0]


    def get_all_adjacent_territories(self, territories: list[int]) -> list[int]:
        result = []
        for territory in territories:
            result.extend(self.map.get_adjacent_to(territory))

        return list(set(result) - set(territories))
