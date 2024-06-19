from typing import Literal, final

from pydantic import BaseModel
from engine.game.state import State
from engine.models.card_model import CardModel
from engine.records.base_record import BaseRecord


@final
class RecordPlayerEliminated(BaseRecord):
    record_type: Literal["record_player_eliminated"] = "record_player_eliminated"
    attack_record: int
    cards_surrendered: list[CardModel]

    def get_public_record(self):
        return PublicRecordPlayerEliminated(attack_record=self.attack_record, cards_surrendered_count=len(self.cards_surrendered))

    def commit(self, state: State) -> None:
        state.match_history.append(self)


class PublicRecordPlayerEliminated(BaseModel):
    attack_record: int
    cards_surrendered_count: int