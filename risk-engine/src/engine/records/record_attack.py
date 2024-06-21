import random
from typing import Literal, cast, final
from engine.game.state import State
from engine.records.base_record import BaseRecord
from engine.records.moves.move_attack import MoveAttack
from engine.records.moves.move_defend import MoveDefend
from engine.records.record_player_eliminated import RecordPlayerEliminated
from engine.records.record_territory_conquered import RecordTerritoryConquered

@final
class RecordAttack(BaseRecord):
    record_type: Literal["record_attack"] = "record_attack"
    move_attack_id: int
    move_defend_id: int
    attacking_troops_lost: int
    defending_troops_lost: int
    territory_conquered: bool
    defender_eliminated: bool

    def get_censored(self, player_id: int):
        return self