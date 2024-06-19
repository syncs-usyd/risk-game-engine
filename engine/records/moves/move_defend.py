from typing import Literal, final
from pydantic import ValidationInfo, model_validator

from engine.game.state import State
from engine.records.base_move import BaseMove

@final
class MoveDefend(BaseMove):
    record_type: Literal["move_defend"] = "move_defend"
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

    def get_public_record(self):
        return self

    def commit(self, state: State) -> None:
        raise NotImplementedError
