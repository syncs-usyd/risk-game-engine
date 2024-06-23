from typing import Literal, final

from risk_shared.records.base_move import BaseMove


@final
class MoveTroopsAfterAttack(BaseMove):
    record_type: Literal["move_troops_after_attack"] = "move_troops_after_attack"
    record_attack_id: int
    troop_count: int






