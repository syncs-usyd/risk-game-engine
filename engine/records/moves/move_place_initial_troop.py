from typing import Literal, final
from pydantic import ValidationInfo, field_validator

from engine.game.state import State
from engine.records.base_move import BaseMove

@final
class MovePlaceInitialTroop(BaseMove):
    record_type: Literal["move_place_initial_troop"] = "move_place_initial_troop"
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
    
    def get_public_record(self, player_id: int):
        return self

    def commit(self, state: State) -> None:
        state.match_history.append(self)
        state.territories[self.territory_id].troops += 1
        state.players[self.move_by_player].troops_remaining -= 1
