from typing import Literal, final
from pydantic import ValidationInfo, field_validator

from engine.game.state import State
from engine.records.base_move import BaseMove

@final
class MoveClaimTerritory(BaseMove):
    record_type: Literal["move_claim_territory"] = "move_claim_territory"
    territory_id: int

    @field_validator("territory_id")
    @classmethod
    def _check_territory_unclaimed(cls, v: int, info: ValidationInfo):
        state = info.context["state"] # type: ignore

        if not v in state.territories:
            raise ValueError(f"You tried to claim a nonexistant territory with id {v}.")
        
        if state.territories[v].occupier != None:
            raise ValueError(f"You tried to claim a territory that is already claimed.")  
        
        return v

    def get_censored(self, player_id: int):
        return self