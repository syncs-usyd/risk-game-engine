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
    record_attack: int
    cards_surrendered: list[CardModel]

    @classmethod
    def factory(cls, state: State, record_attack: int, player: int) -> 'RecordPlayerEliminated':
        cards_surrendered = list(state.players[player].cards).copy()
        return cls(player=player, record_attack=record_attack, cards_surrendered=cards_surrendered)

    def get_public_record(self):
        return PublicRecordPlayerEliminated(record_attack=self.record_attack, cards_surrendered_count=len(self.cards_surrendered))

    def commit(self, state: State) -> None:
        state.match_history.append(self)


class PublicRecordPlayerEliminated(BaseModel):
    record_attack: int
    cards_surrendered_count: int