from typing import Optional
from pydantic import BaseModel


class CardModel(BaseModel):
    territory_id: int
    occupier: Optional[int]
    troops_count: int
    troop_type: str
