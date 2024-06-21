from typing import Literal, final

from risk_shared.records.base_move import BaseMove

@final
class MoveDefend(BaseMove):
    record_type: Literal["move_defend"] = "move_defend"
    move_attack_id: int
    defending_troops: int

    def get_censored(self, player_id: int):
        return self
