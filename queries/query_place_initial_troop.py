from typing import Iterable, Literal
from pydantic import BaseModel

from models.player.player_private_model import PlayerPrivateModel
from models.player.player_public_model import PlayerPublicModel
from models.territory_model import TerritoryModel


class QueryPlaceInitialTroop(BaseModel):
    query: Literal["place_initial_troop"] = "place_initial_troop"
    territories: Iterable[TerritoryModel]
    players: Iterable[PlayerPublicModel] 