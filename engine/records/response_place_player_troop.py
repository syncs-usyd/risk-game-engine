from pydantic import BaseModel, ValidationInfo, field_validator


class ResponsePlacePlayerTroop(BaseModel):
    territory_id: int
    troop_count: int

    @field_validator("territory_id")
    @classmethod
    def _check_territory_occupied(cls, v: int, info: ValidationInfo):
        state = info.context["state"] # type: ignore
        player = info.context["player"] # type: ignore

        if not v in state.territories:
            raise ValueError(f"No territory exists with territory_id {v}.")
        
        if state.territories[v].occupier != player:
            raise ValueError(f"You don't occupy this territory.")  
        
        return v
    
    @field_validator("troop_count")
    @classmethod
    def _check_troop_count(cls, v: int, info: ValidationInfo):
        player = info.context["player"] # type: ignore

        if v < 1:
            raise ValueError("Troop count must be at least 1.")
        
        if v > player.troops:
            raise ValueError("You don't have enough troops to place.")
        
        return v