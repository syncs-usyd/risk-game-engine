from typing import List
from pydantic import BaseModel, ValidationInfo, field_validator

# NOTE: Not sure yet if the input of the player should be the territory id or territory name
# So far it is territory id

class ResponseRedeemPlayerCards(BaseModel):
    territory_id: List[int]

    @field_validator("territory_id")
    @classmethod
    def _check_redeem_player_cards(cls, v: List[int], info: ValidationInfo):
        state = info.context["state"] # type: ignore
        player = info.context["player"] # type: ignore

        for i in v:
            if not i in state.territories:
                raise ValueError(f"No territory exists with territory_id {i}.")
            
            if state.territories[i].occupier != player:
                raise ValueError(f"You don't occupy this territory.")  
        
        return v