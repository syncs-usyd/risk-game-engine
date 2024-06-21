from typing import Literal, final
from engine.game.state import State
from engine.records.base_record import BaseRecord

@final
class RecordStartTurn(BaseRecord):
    record_type: Literal["record_start_turn"] = "record_start_turn"
    player: int
    continents_held: list[int]
    territories_held: int
    continent_bonus: int
    territory_bonus: int

    def get_censored(self, player_id: int):
        return self
