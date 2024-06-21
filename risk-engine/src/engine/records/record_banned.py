from typing import Literal, Union, final

from pydantic import BaseModel
from engine.exceptions import BrokenPipeException, CumulativeTimeoutException, InvalidResponseException, PlayerException, TimeoutException
from engine.game.state import State
from engine.models.card_model import CardModel
from engine.output.ban_type import BanType
from engine.records.base_record import BaseRecord

@final
class RecordBanned(BaseRecord):
    record_type: Literal["record_banned"] = "record_banned"
    player: int
    ban_type: BanType
    reason: str

    def get_censored(self, player_id: int):
        return self