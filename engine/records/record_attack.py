from typing import Literal, final
from engine.game.state import State
from engine.records.base_record import BaseRecord

@final
class RecordAttack(BaseRecord):
    record_type: Literal["record_attack"] = "record_attack"
    attack_move: int
    defend_move: int
    attacking_troops_lost: int
    defending_troops_lost: int
    territory_conquered: bool
    defender_eliminated: bool

    def get_public_record(self):
        return self

    def commit(self, state: State) -> None:
        raise NotImplementedError
