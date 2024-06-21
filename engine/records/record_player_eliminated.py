from typing import Literal, cast, final

from pydantic import BaseModel
from engine.game.state import State
from engine.models.card_model import CardModel
from engine.records.base_record import BaseRecord
from engine.records.moves.move_defend import MoveDefend
from engine.records.record_attack import RecordAttack


@final
class RecordPlayerEliminated(BaseRecord):
    record_type: Literal["record_player_eliminated"] = "record_player_eliminated"
    player: int
    record_attack_id: int
    cards_surrendered: list[CardModel]

    @classmethod
    def factory(cls, state: State, record_attack_id: int, player: int) -> 'RecordPlayerEliminated':
        cards_surrendered = list(state.players[player].cards).copy()
        return cls(player=player, record_attack_id=record_attack_id, cards_surrendered=cards_surrendered)

    def get_public_record(self, player_id: int):
        if self.player == player_id:
            return self
        return PublicRecordPlayerEliminated(record_attack=self.record_attack_id, cards_surrendered_count=len(self.cards_surrendered))

    def commit(self, state: State) -> None:
        state.recording.append(self)


@final
class PublicRecordPlayerEliminated(BaseRecord):
    record_type: Literal["record_player_eliminated"] = "record_player_eliminated"
    record_attack: int
    cards_surrendered_count: int

    def get_public_record(self, player_id: int):
        return self

    def commit(self, state: State) -> None:
        raise NotImplementedError
