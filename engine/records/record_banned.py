from typing import Literal, final

from pydantic import BaseModel
from engine.game.state import State
from engine.models.card_model import CardModel
from engine.records.base_record import BaseRecord

@final
class RecordDrewCard(BaseRecord):
    record_type: Literal["record_banned"] = "record_banned"
    player: int
    reason: str

    def get_public_record(self, player_id: int):
        return self

    def commit(self, state: State) -> None:
        raise NotImplementedError