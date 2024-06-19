from typing import Literal, final
from engine.game.state import State
from engine.records.base_record import BaseRecord

@final
class RecordTurnOrder(BaseRecord):
    record_type: Literal["record_turn_order"] = "record_turn_order"
    turn_order: list[int]

    def get_public_record(self):
        return self

    def commit(self, state: State) -> None:
        state.match_history.append(self)
        state.turn_order = self.turn_order.copy()
