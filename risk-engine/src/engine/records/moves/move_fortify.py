from typing import Literal, final
from pydantic import ValidationInfo, model_validator

from engine.game.state import State
from engine.records.base_move import BaseMove

@final
class MoveFortify(BaseMove):
    record_type: Literal["move_fortify"] = "move_fortify"
    source_territory: int
    target_territory: int
    troop_count: int

    @model_validator(mode='after')
    def _check_troops(self, info: ValidationInfo):
        state = info.context['state'] # type: ignore
        player = info.context['player'] # type: ignore

        if not self.source_territory in state.territories:
            raise ValueError(f"Your source territory with id {self.source_territory} does not exist.")

        if not self.target_territory in state.territories:
            raise ValueError(f"Your target territory with id {self.source_territory} does not exist.")
        
        if state.territories[self.source_territory].occupier != player:
            raise ValueError(f"You don't occupy the source territory.")

        if state.territories[self.target_territory].occupier != player:
            raise ValueError(f"You don't occupy the target territory.")
        
        if not state.map.is_adjacent(self.source_territory, self.target_territory):
            raise ValueError(f"Your target territory {self.target_territory} is not adjacent to your source territory {self.source_territory}.")
        
        if not 0 <= self.troop_count <= state.territories[self.source_territory].troops - 1:
            raise ValueError(f"You tried to move {self.troop_count} troops, you must move between zero and the number of troops in the source territory, subtracting one troop which must be left behind.")
        
        return self

    def get_censored(self, player_id: int):
        return self

    




