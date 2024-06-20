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

    def get_public_record(self, player_id: int):
        return PublicRecordDrewCard(player=self.player)

    def commit(self, state: State) -> None:
        raise NotImplementedError


@final
class PublicRecordDrewCard(BaseRecord):
    record_type: Literal["public_record_drew_card"] = "public_record_drew_card"
    player: int

    def get_public_record(self, player_id: int):
        return self

    def commit(self, state: State) -> None:
        raise NotImplementedError
