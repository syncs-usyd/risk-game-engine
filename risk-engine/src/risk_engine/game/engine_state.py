import json
from risk_engine.config.gameconfig import NUM_PLAYERS, NUM_STARTING_TROOPS
from risk_engine.config.ioconfig import CORE_DIRECTORY
from risk_shared.maps.map import Map
from risk_shared.maps import earth
from risk_shared.models.card_model import CardModel
from risk_shared.models.player_model import PlayerModel
from risk_shared.models.territory_model import TerritoryModel
from risk_shared.records.types.record_type import RecordType

class EngineState():
    def __init__(self):
        with open(f"{CORE_DIRECTORY}/input/catalog.json", "r") as f:
            catalog = json.load(f)

        self.map: Map = earth.create_map()
        self.cards: dict[int, CardModel] = dict([(i, card) for i, card in earth.create_cards().items()])
        self.deck: list[CardModel] = []
        self.discarded_deck: list[CardModel] = list(self.cards.values())
        self.players: dict[int, PlayerModel] = dict([(x, PlayerModel(player_id=x, team_id=catalog[x]["team_id"], troops_remaining=NUM_STARTING_TROOPS, alive=True, cards=[], must_place_territory_bonus=[])) for x in range(NUM_PLAYERS)])
        self.territories: dict[int, TerritoryModel] = dict([(x, TerritoryModel(territory_id=x, occupier=None, troops=0)) for x in self.map.get_vertices()])
        self.card_sets_redeemed: int = 0
        self.turn_order: list[int] = [x.player_id for x in self.players.values()]
        self.recording: list[RecordType] = []