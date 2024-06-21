from typing import Literal, final
from risk_shared.output.ban_type import BanType
from risk_shared.records.base_record import BaseRecord

@final
class RecordBanned(BaseRecord):
    record_type: Literal["record_banned"] = "record_banned"
    player: int
    ban_type: BanType
    reason: str

    def get_censored(self, player_id: int):
        return self