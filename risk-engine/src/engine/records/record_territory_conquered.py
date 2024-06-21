from typing import Literal, cast, final

from engine.game.state import State
from engine.records.base_record import BaseRecord
from engine.records.moves.move_attack import MoveAttack

@final
class RecordTerritoryConquered(BaseRecord):
    record_type: Literal["record_territory_conquered"] = "record_territory_conquered"
    record_attack_id: int

    def get_censored(self, player_id: int):
        return self

