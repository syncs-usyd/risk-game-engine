from typing import Literal, final

from risk_shared.records.base_move import BaseMove

@final
class MoveFortify(BaseMove):
    record_type: Literal["move_fortify"] = "move_fortify"
    source_territory: int
    target_territory: int
    troop_count: int

    




