from typing import Literal, Iterable

from engine.models.territory_model import TerritoryModel
from engine.models.player.player_public_model import PlayerPublicModel
from engine.queries.base_query import BaseQuery

class QueryFortifyTerritory(BaseQuery):
    query_type: Literal["fortify_territory"] = "fortify_territory"
    territories: Iterable[TerritoryModel]
    players: Iterable[PlayerPublicModel]