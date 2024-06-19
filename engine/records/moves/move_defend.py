from pydantic import BaseModel, ValidationInfo, model_validator


class MoveDefend(BaseModel):
    territory_id: int
    num_troops: int

    @model_validator(mode="after")
    def _check_territory_occupied(self: 'MoveDefend', info: ValidationInfo) -> 'MoveDefend':
        state: GameState = info.context["state"] # type: ignore

        if not 1 <= self.num_troops <= 2:
            raise ValueError(f"You must commit 1 or 2 troops for the defence.")
        if state.territories[self.territory_id].troops < self.num_troops:
            raise ValueError(f"You tried to defend with more troops then you had occupying the defending territory.")
        
        return self