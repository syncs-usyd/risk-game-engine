from pydantic import BaseModel, ValidationInfo, field_validator


class MoveDistributeTroops(BaseModel):
    distributions: dict[int, int] # territory_id, troop_count

    @field_validator("territory_id")
    @classmethod
    def _check_territory_occupied(cls, distributions: dict[int, int], info: ValidationInfo):
        state = info.context["state"] # type: ignore
        player = info.context["player"] # type: ignore

        for territory in distributions:
            if not territory in state.territories:
                raise ValueError(f"You tried to claim a nonexistant territory with id {territory}.")
            
            if state.territories[territory].occupier != player:
                raise ValueError("You don't occupy this territory.")  
            
        return distributions
    
    @field_validator("troop_count")
    @classmethod
    def _check_troop_count(cls, distributions: dict[int, int], info: ValidationInfo):
        player = info.context["player"] # type: ignore

        if sum(distributions.values()) != player.troops:
            raise ValueError(f"You must distribute exactly your remaining {player.troops} troops.")