from typing import Literal, final

from engine.game.state import State
from engine.records.base_record import BaseRecord

@final
class RecordTerritoryConquered(BaseRecord):
    record_type: Literal["record_territory_conquered"] = "record_territory_conquered"
    attack_record: int

    def get_public_record(self):
        return self

    def commit(self, state: State) -> None:
        state.match_history.append(self)
