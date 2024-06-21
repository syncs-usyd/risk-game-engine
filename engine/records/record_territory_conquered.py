from typing import Literal, cast, final

from engine.game.state import State
from engine.records.base_record import BaseRecord
from engine.records.moves.move_attack import MoveAttack

@final
class RecordTerritoryConquered(BaseRecord):
    record_type: Literal["record_territory_conquered"] = "record_territory_conquered"
    record_attack_id: int

    def get_public_record(self, player_id: int):
        return self

    def commit(self, state: State) -> None:
        state.recording.append(self)

        move_attack_obj = cast(MoveAttack, state.recording[self.record_attack_id])
        if move_attack_obj.move == "pass":
            raise RuntimeError("Tried to record territory conquered for attack that was a pass.")

        defending_territory = move_attack_obj.move.defending_territory

        state.territories[defending_territory].troops = 0
        state.territories[defending_territory].occupier = move_attack_obj.move_by_player

