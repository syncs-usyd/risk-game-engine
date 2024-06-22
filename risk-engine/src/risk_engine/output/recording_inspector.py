

from typing import Iterable, Union

from pydantic import BaseModel, RootModel
from risk_engine.output.game_result import GameBanResult, GameCancelledResult, GameSuccessResult
from risk_shared.records.record_banned import RecordBanned
from risk_shared.records.record_cancelled import RecordCancelled
from risk_shared.records.record_player_eliminated import RecordPlayerEliminated
from risk_shared.records.record_winner import RecordWinner
from risk_shared.records.types.record_type import RecordType


class RecordingInspector():

    def __init__(self, recording: list[RecordType]):
        self.recording = recording


    def _get_ranking(self) -> list[int]:
        ranking = []
        for record in self.recording:
            match record:
                case RecordPlayerEliminated() as x:
                    ranking.append(x.player)
                case RecordWinner() as x:
                    ranking.append(x.player)

        return ranking[::-1]


    def get_result(self) -> Union[GameBanResult, GameSuccessResult, GameCancelledResult]:
        match self.recording[-1]:
            case RecordCancelled() as x:
                return GameCancelledResult(reason=x.reason)
            case RecordBanned() as x:
                return GameBanResult(result_type=x.ban_type, player=x.player, reason=x.reason)
            case RecordWinner() as x:
                return GameSuccessResult(ranking=self._get_ranking())
            case _:
                raise NotImplementedError
            

    def get_recording_json(self) -> str:
        return RootModel(self.recording).model_dump_json()