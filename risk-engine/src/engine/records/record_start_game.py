from typing import Literal, Sequence, final
from engine.game.state import State
from engine.models.player.player_model import PublicPlayerModel
from engine.records.base_record import BaseRecord

@final
class RecordStartGame(BaseRecord):
    record_type: Literal["record_start_game"] = "record_start_game"
    turn_order: Sequence[int]
    players: Sequence[PublicPlayerModel]

    def get_censored(self, player_id: int):
        return self