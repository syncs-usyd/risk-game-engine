from typing import Literal, final

from risk_shared.records.base_record import BaseRecord

@final
class RecordWinner(BaseRecord):
    record_type: Literal["record_winner"] = "record_winner"
    player: int

    def get_censored(self, player_id: int):
        return self