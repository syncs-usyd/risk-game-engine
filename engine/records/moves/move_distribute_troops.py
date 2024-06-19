from typing import Literal, final
from pydantic import ValidationInfo, field_validator

from engine.game.state import State
from engine.records.base_move import BaseMove

@final
class MoveDistributeTroops(BaseMove):
    record_type: Literal["move_distribute_troops"] = "move_distribute_troops"
    distributions: dict[int, int] # territory_id, troop_count

    @field_validator("distributions")
    @classmethod
    def _check_troop_distributions(cls, distributions: dict[int, int], info: ValidationInfo):
        state = info.context["state"] # type: ignore
        player = info.context["player"] # type: ignore

        for territory in distributions:
            if not territory in state.territories:
                raise ValueError(f"You tried to claim a nonexistant territory with id {territory}.")
            
            if state.territories[territory].occupier != player:
                raise ValueError("You don't occupy this territory.")  
            
        if sum(distributions.values()) != player.troops:
            raise ValueError(f"You must distribute exactly your remaining {player.troops} troops.")
            
        return distributions

    def get_public_record(self):
        return self

    def commit(self, state: State) -> None:
        raise NotImplementedError

        