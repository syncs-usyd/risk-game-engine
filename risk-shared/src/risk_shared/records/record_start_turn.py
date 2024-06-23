from typing import Literal, final
from risk_shared.records.base_record import BaseRecord

@final
class RecordStartTurn(BaseRecord):
    record_type: Literal["record_start_turn"] = "record_start_turn"
    player: int
    continents_held: list[int]
    territories_held: int
    continent_bonus: int
    territory_bonus: int
