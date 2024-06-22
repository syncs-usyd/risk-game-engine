from risk_shared.maps import earth
from risk_shared.models.card_model import CardModel
from risk_shared.models.player_model import PlayerModel, PublicPlayerModel
from risk_shared.models.territory_model import TerritoryModel
from risk_shared.records.types.record_type import RecordType


class State():

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
        self.me: PlayerModel

    