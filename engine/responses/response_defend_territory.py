from pydantic import BaseModel, ValidationInfo, field_validator


class ResponseDefendTerritory(BaseModel):
    territory_id: int
    num_troops: int

    @field_validator("territory_id")
    @classmethod
    def _check_territory_occupied(cls, territory_id: int, num_troops: int, info: ValidationInfo):
        state = info.context["state"] # type: ignore
        player = info.context["player"] # type: ignore

        if num_troops < 0 or num_troops > 2:
            raise ValueError(f"You must commit 1 or 2 troops for the defence.")
        if state.territores[territory_id].troops < num_troops:
            raise ValueError(f"You tried to defend with 2 troops when you only had one.")
        

        return v