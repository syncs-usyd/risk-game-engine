from typing import Literal
from pydantic import BaseModel

from risk_shared.output.ban_type import BanType

class GameBanResult(BaseModel):
    result_type: Literal["PLAYER_BANNED"] = "PLAYER_BANNED"
    ban_type: BanType
    player: int
    reason: str


class GameSuccessResult(BaseModel):
    result_type: Literal["SUCCESS"] = "SUCCESS"
    ranking: list[int]


class GameCancelledResult(BaseModel):
    result_type: Literal["CANCELLED"] = "CANCELLED"
    reason: str

class GameCrashedResult(BaseModel):
    result_type: Literal["CRASHED"] = "CRASHED"
    reason: str