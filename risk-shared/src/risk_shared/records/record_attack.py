from typing import Literal, final
from risk_shared.records.base_record import BaseRecord

@final
class RecordAttack(BaseRecord):
    record_type: Literal["record_attack"] = "record_attack"
    move_attack_id: int
    move_defend_id: int
    attacking_troops_lost: int
    defending_troops_lost: int
    territory_conquered: bool
    defender_eliminated: bool