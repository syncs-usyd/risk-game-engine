from pydantic import BaseModel

from engine.models.card_model import CardModel


class RecordDrewCard(BaseModel):
    player: int

class PrivateRecordDrewCard(RecordDrewCard):
    card: CardModel