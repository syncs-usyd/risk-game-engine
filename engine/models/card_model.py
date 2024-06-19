from typing import Literal, Optional, Union
from pydantic import BaseModel


class CardModel(BaseModel):
    card_id: int
    territory_id: Optional[int]
    symbol: Union[Literal["Infantry"], Literal["Cavalry"], Literal["Artillery"], Literal["Wildcard"]]

