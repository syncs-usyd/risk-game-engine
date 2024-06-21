

from typing import Literal, Union
from pydantic import BaseModel

from engine.output.ban_type import BanType

class GameBanResult(BaseModel):
    result_type: BanType
    player: int
    reason: str


class GameSuccessResult(BaseModel):
    result_type: Literal["SUCCESS"] = "SUCCESS"
    ranking: list[int]


class GameCancelledResult(BaseModel):
    result_type: Literal["CANCELLED"] = "CANCELLED"