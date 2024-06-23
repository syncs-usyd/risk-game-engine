from typing import Literal, final
from risk_shared.models.card_model import CardModel
from risk_shared.records.base_record import BaseRecord

@final
class RecordDrewCard(BaseRecord):
    record_type: Literal["record_drew_card"] = "record_drew_card"
    player: int
    card: CardModel


@final
class PublicRecordDrewCard(BaseRecord):
    record_type: Literal["public_record_drew_card"] = "public_record_drew_card"
    player: int
