from typing import Literal, final

from risk_shared.records.base_move import BaseMove

@final
class MoveFortifyPass(BaseMove):
    record_type: Literal["move_fortify_pass"] = "move_fortify_pass"
