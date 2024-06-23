from typing import Literal, Sequence, final
from risk_shared.models.player_model import PlayerModel, PublicPlayerModel
from risk_shared.records.base_record import BaseRecord

@final
class RecordStartGame(BaseRecord):
    record_type: Literal["record_start_game"] = "record_start_game"
    turn_order: Sequence[int]
    players: Sequence[PlayerModel]

@final
class PublicRecordStartGame(BaseRecord):
    record_type: Literal["public_record_start_game"] = "public_record_start_game"
    turn_order: Sequence[int]
    players: Sequence[PublicPlayerModel]
    you: PlayerModel