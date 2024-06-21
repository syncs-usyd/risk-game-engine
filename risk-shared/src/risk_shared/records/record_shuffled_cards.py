from typing import Literal, final
from risk_shared.records.base_record import BaseRecord

@final
class RecordShuffledCards(BaseRecord):
    record_type: Literal["record_shuffled_cards"] = "record_shuffled_cards"

    def get_censored(self, player_id: int):
        return self
