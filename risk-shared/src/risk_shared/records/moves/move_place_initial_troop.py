from typing import Literal, final

from risk_shared.records.base_move import BaseMove

@final
class MovePlaceInitialTroop(BaseMove):
    record_type: Literal["move_place_initial_troop"] = "move_place_initial_troop"
    territory: int