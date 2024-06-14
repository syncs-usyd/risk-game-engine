from typing import Optional
from pydantic import BaseModel


class TerritoryModel(BaseModel):
    territory_id: int
    occupier: Optional[int]
    troops: int