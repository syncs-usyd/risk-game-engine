from pydantic import BaseModel

from engine.models.card_model import CardModel


class RecordPlayerEliminated(BaseModel):
    attack_record: int

class PrivateRecordPlayerEliminated(RecordPlayerEliminated):
    card_surrendered: list[CardModel]