from pydantic import BaseModel, ValidationInfo, field_validator


class MovePlaceInitialTroop(BaseModel):
    territory_id: int

    @field_validator("territory_id")
    @classmethod
    def _check_territory_occupied(cls, v: int, info: ValidationInfo):
        state = info.context["state"] # type: ignore
        player = info.context["player"] # type: ignore

        if not v in state.territories:
            raise ValueError(f"You tried to claim a nonexistant territory with id {v}.")
        
        if state.territories[v].occupier != player:
            raise ValueError(f"You don't occupy this territory.")  
        
        return v