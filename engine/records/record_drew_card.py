from typing import Literal, final

from pydantic import BaseModel
from engine.game.state import State
from engine.models.card_model import CardModel
from engine.records.base_record import BaseRecord

@final
class RecordDrewCard(BaseRecord):
    record_type: Literal["record_drew_card"] = "record_drew_card"
    player: int
    card: CardModel

    def get_public_record(self):
        return PublicRecordDrewCard.model_validate(self.model_dump())

    def commit(self, state: State) -> None:
        raise NotImplementedError


class PublicRecordDrewCard(BaseModel):
    player: int