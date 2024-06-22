from typing import Literal, final

from risk_shared.records.base_record import BaseRecord

@final
class RecordCancelled(BaseRecord):
    record_type: Literal["record_cancelled"] = "record_cancelled"
    reason: str

    def get_censored(self, player_id: int):
        return self