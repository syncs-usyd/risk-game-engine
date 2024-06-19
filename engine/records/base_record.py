from abc import ABC, abstractmethod
from pydantic import BaseModel
from engine.game.state import State

class BaseRecord(BaseModel, ABC):
    record_type: str

    @abstractmethod
    def get_public_record(self):
        pass

    @abstractmethod
    def commit(self, state: State) -> None:
        pass