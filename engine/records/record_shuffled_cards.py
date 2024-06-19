import random
from typing import Literal, final
from engine.game.state import State
from engine.records.base_record import BaseRecord

@final
class RecordShuffledCards(BaseRecord):
    record_type: Literal["record_shuffled_cards"] = "record_shuffled_cards"

    def get_public_record(self):
        return self

    def commit(self, state: State) -> None:
        state.match_history.append(self)

        if len(state.deck) != 0:
            raise RuntimeError("Shuffled cards before deck was empty.")

        state.deck = state.discarded_deck
        random.shuffle(state.deck)
