from typing import Iterable, Literal

from engine.models.player.player_public_model import PlayerPublicModel
from engine.models.territory_model import TerritoryModel
from engine.queries.base_query import BaseQuery


class QueryRedeemPlayerCards(BaseQuery):
    query_type: Literal["place_player_troop"] = "place_player_troop"
    territories: Iterable[TerritoryModel]
    players: Iterable[PlayerPublicModel]