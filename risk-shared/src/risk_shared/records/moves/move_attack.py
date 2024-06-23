from typing import Literal, Union, final
from pydantic import BaseModel

from risk_shared.records.base_move import BaseMove

class MoveAttackDescription(BaseModel):
    attacking_territory: int
    defending_territory: int
    attacking_troops: int

@final
class MoveAttack(BaseMove):
    record_type: Literal["move_attack"] = "move_attack"
    move: Union[MoveAttackDescription, Literal["pass"]]
