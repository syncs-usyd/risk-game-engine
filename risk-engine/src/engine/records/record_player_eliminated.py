from typing import Literal, final

from engine.game.state import State
from engine.models.card_model import CardModel
from engine.records.base_record import BaseRecord


@final
class RecordPlayerEliminated(BaseRecord):
    record_type: Literal["record_player_eliminated"] = "record_player_eliminated"
    player: int
    record_attack_id: int
    cards_surrendered: list[CardModel]

    def get_censored(self, player_id: int):
        if self.player == player_id:
            return self
        return PublicRecordPlayerEliminated(record_attack=self.record_attack_id, cards_surrendered_count=len(self.cards_surrendered))


@final
class PublicRecordPlayerEliminated(BaseRecord):
    record_type: Literal["record_player_eliminated"] = "record_player_eliminated"
    record_attack: int
    cards_surrendered_count: int

    def get_censored(self, player_id: int):
        return self
