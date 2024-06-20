from typing import Literal, cast, final
from pydantic import ValidationInfo, field_validator, model_validator

from engine.game.state import State
from engine.queries.query_troops_after_attack import QueryTroopsAfterAttack
from engine.records.base_move import BaseMove
from engine.records.moves.move_attack import MoveAttack
from engine.records.record_attack import RecordAttack

@final
class MoveTroopsAfterAttack(BaseMove):
    record_type: Literal["move_troops_after_attack"] = "move_troops_after_attack"
    record_attack_id: int
    troop_count: int
    
    @model_validator(mode="after")
    def _check_troop_count(self, info: ValidationInfo):
        state: State = info.context["state"] # type: ignore
        query: QueryTroopsAfterAttack = info.context["context"] # type: ignore
        
        if self.record_attack_id != query.record_attack_id:
            raise ValueError(f"You must move troops for the attack record with id {query.record_attack_id}.")

        record_attack = cast(RecordAttack, state.match_history[self.record_attack_id])

        move_attack_id = record_attack.move_attack_id
        move_attack = cast(MoveAttack, state.match_history[move_attack_id])
        if move_attack.move == "pass":
            raise RuntimeError("Trying to move troops for attack that was a pass.")

        minimum_troops_moved = move_attack.move.attacking_troops - record_attack.attacking_troops_lost

        if not minimum_troops_moved <= self.troop_count:
            raise ValueError("You must move troops from the attacking territory to the defending territory after a successful attack, depending on how many troops were committed and how many died.")
        
        if not self.troop_count <= cast(int, state.territories[move_attack.move.attacking_territory]) - 1:
            raise ValueError(f"You tried to move too many troops from territory {move_attack.move.attacking_territory}.")

        return self
    
    def get_public_record(self, player_id: int):
        return self

    def commit(self, state: State) -> None:
        state.match_history.append(self)

        record_attack = cast(RecordAttack, state.match_history[self.record_attack_id])

        move_attack_id = record_attack.move_attack_id
        move_attack = cast(MoveAttack, state.match_history[move_attack_id])
        if move_attack.move == "pass":
            raise RuntimeError("Trying to move troops for attack that was a pass.")
        
        state.territories[move_attack.move.attacking_territory].troops -= self.troop_count
        state.territories[move_attack.move.defending_territory].troops += self.troop_count






