from typing import Literal, final

from risk_shared.records.base_move import BaseMove

@final
class MoveAttackPass(BaseMove):
    record_type: Literal["move_attack_pass"] = "move_attack_pass"