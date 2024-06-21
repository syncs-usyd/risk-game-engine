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

    @classmethod
    def factory(cls, e: PlayerException) -> 'RecordBanned':
        ban_type: BanType
        match e:
            case TimeoutException():
                ban_type = "TIMEOUT"
            case CumulativeTimeoutException():
                ban_type = "CUMULATIVE_TIMEOUT"
            case BrokenPipeException():
                ban_type = "BROKEN_PIPE"
            case InvalidResponseException():
                ban_type = "INVALID_MOVE"

            case _:
                raise RuntimeError("An unspecified PlayerException was raised.")

        return cls(player=e.player_id, reason=e.error_message, ban_type=ban_type)

    def get_public_record(self, player_id: int):
        return self

    def commit(self, state: State) -> None:
        state.recording.append(self)