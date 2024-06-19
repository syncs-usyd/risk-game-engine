from typing import Literal, Iterable
from pydantic import BaseModel

from engine.models.territory_model import TerritoryModel
from engine.models.player.player_public_model import PlayerPublicModel

class QueryFortifyTerritory(BaseModel):
    query: Literal["fortify_territory"] = "fortify_territory"
    territories: Iterable[TerritoryModel]
    players: Iterable[PlayerPublicModel]