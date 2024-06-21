from typing import Literal, final
from risk_shared.models.card_model import CardModel
from risk_shared.records.base_record import BaseRecord

@final
class RecordDrewCard(BaseRecord):
    record_type: Literal["record_drew_card"] = "record_drew_card"
    player: int
    card: CardModel

    def get_censored(self, player_id: int):
        if self.player == player_id:
            return self
        return PublicRecordDrewCard(player=self.player)


@final
class PublicRecordDrewCard(BaseRecord):
    record_type: Literal["public_record_drew_card"] = "public_record_drew_card"
    player: int

    def get_censored(self, player_id: int):
        return self
