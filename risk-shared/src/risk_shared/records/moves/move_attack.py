from typing import Literal, final
from risk_shared.records.base_move import BaseMove

@final
class MoveAttack(BaseMove):
    record_type: Literal["move_attack"] = "move_attack"
    attacking_territory: int
    defending_territory: int
    attacking_troops: int
