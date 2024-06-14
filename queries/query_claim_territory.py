from typing import Iterable, Literal
from pydantic import BaseModel

from models.player.player_private_model import PlayerPrivateModel
from models.player.player_public_model import PlayerPublicModel
from models.territory_model import TerritoryModel


class QueryClaimTerritory(BaseModel):
    query: Literal["claim_territory"] = "claim_territory"
    territories: Iterable[TerritoryModel]
    players: Iterable[PlayerPublicModel]