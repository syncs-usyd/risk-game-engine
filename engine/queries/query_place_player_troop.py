from typing import Iterable, Literal
from pydantic import BaseModel

from engine.models.player.player_private_model import PlayerPrivateModel
from engine.models.player.player_public_model import PlayerPublicModel
from engine.models.territory_model import TerritoryModel


class QueryPlacePlayerTroop(BaseModel):
    query: Literal["place_player_troop"] = "place_player_troop"
    territories: Iterable[TerritoryModel]
    players: Iterable[PlayerPublicModel]