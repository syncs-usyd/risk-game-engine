from typing import Literal, final

from risk_shared.records.base_move import BaseMove

@final
class MoveClaimTerritory(BaseMove):
    record_type: Literal["move_claim_territory"] = "move_claim_territory"
    territory: int