from typing import Iterable, Literal
from pydantic import BaseModel

from engine.models.player.player_private_model import PlayerPrivateModel
from engine.models.player.player_public_model import PlayerPublicModel
from engine.models.territory_model import TerritoryModel


class QueryClaimTerritory(BaseModel):
    query: Literal["claim_territory"] = "claim_territory"
    territories: Iterable[TerritoryModel]
    players: Iterable[PlayerPublicModel]