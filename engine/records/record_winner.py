from typing import Literal, final

from pydantic import BaseModel
from engine.game.state import State
from engine.models.card_model import CardModel
from engine.records.base_record import BaseRecord

@final
class RecordWinner(BaseRecord):
    record_type: Literal["record_winner"] = "record_winner"
    player: int

    def get_public_record(self, player_id: int):
        return self

    def commit(self, state: State) -> None:
        state.recording.append(self)