from pydantic import BaseModel, ValidationInfo, field_validator


class MoveClaimTerritory(BaseModel):
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