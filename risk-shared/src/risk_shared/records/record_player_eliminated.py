from typing import Literal, final
from risk_shared.models.card_model import CardModel
from risk_shared.records.base_record import BaseRecord

@final
class RecordPlayerEliminated(BaseRecord):
    record_type: Literal["record_player_eliminated"] = "record_player_eliminated"
    player: int
    record_attack_id: int
    cards_surrendered: list[CardModel]

@final
class PublicRecordPlayerEliminated(BaseRecord):
    record_type: Literal["record_player_eliminated"] = "record_player_eliminated"
    player: int
    record_attack_id: int
    cards_surrendered_count: int
