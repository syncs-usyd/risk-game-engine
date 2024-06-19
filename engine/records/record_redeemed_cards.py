from typing import Literal, final
from engine.game.state import State
from engine.records.base_record import BaseRecord

@final
class RecordRedeemedCards(BaseRecord):
    record_type: Literal["record_redeemed_cards"] = "record_redeemed_cards"
    redeem_cards_move: int
    total_set_bonus: int
    matching_territory_bonus: int

    def get_public_record(self):
        return self

    def commit(self, state: State) -> None:
        raise NotImplementedError
