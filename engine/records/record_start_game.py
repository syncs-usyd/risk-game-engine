from typing import Literal, Sequence, final
from engine.game.state import State
from engine.models.player.player_model import PublicPlayerModel
from engine.records.base_record import BaseRecord

@final
class RecordStartGame(BaseRecord):
    record_type: Literal["record_start_game"] = "record_start_game"
    turn_order: Sequence[int]
    players: Sequence[PublicPlayerModel]

    def get_public_record(self, player_id: int):
        return self

    def commit(self, state: State) -> None:
        state.recording.append(self)
        state.turn_order = list(self.turn_order).copy()
