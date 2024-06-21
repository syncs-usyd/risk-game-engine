from abc import ABC, abstractmethod
from pydantic import BaseModel
from engine.game.state import State

class BaseRecord(BaseModel, ABC):
    record_type: str

    @abstractmethod
    def get_censored(self, player_id: int):
        pass