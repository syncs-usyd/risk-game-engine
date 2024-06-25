from typing import Literal, final
from risk_shared.records.base_record import BaseRecord

@final
class RecordRedeemedCards(BaseRecord):
    record_type: Literal["record_redeemed_cards"] = "record_redeemed_cards"
    move_redeem_cards_id: int
    total_set_bonus: int
    matching_territory_bonus: int