import random
from typing import Literal, final
from engine.game.state import State
from engine.records.base_record import BaseRecord

@final
class RecordShuffledCards(BaseRecord):
    record_type: Literal["record_shuffled_cards"] = "record_shuffled_cards"

    def get_censored(self, player_id: int):
        return self
