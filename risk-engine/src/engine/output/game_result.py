from typing import Literal
from pydantic import BaseModel

from risk_shared.output.ban_type import BanType

class GameBanResult(BaseModel):
    result_type: BanType
    player: int
    reason: str


class GameSuccessResult(BaseModel):
    result_type: Literal["SUCCESS"] = "SUCCESS"
    ranking: list[int]


class GameCancelledResult(BaseModel):
    result_type: Literal["CANCELLED"] = "CANCELLED"