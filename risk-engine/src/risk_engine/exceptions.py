from typing import Any, Optional
from risk_shared.queries.query_type import QueryType
from risk_shared.records.types.move_type import MoveType


class PlayerException(Exception):
    def __init__(self, player_id: int, error_message: str):
        super().__init__(error_message)
        self.player_id = player_id
        self.error_message = error_message

class TimeoutException(PlayerException):
    def __init__(self, player_id: int, error_message: str, query: Optional[QueryType]):
        super().__init__(player_id, error_message)
        # if query:
        #     query.update = {}
        self.details = query

class CumulativeTimeoutException(PlayerException):
    def __init__(self, player_id: int, error_message: str, query: Optional[QueryType]):
        super().__init__(player_id, error_message)
        # if query:
        #     query.update = {}
        self.details = query

class BrokenPipeException(PlayerException):
    pass

class InvalidMessageException(PlayerException):
    def __init__(self, player_id: int, error_message: str, details: Optional[list[Any]] = None):
        super().__init__(player_id, error_message)
        self.details = details

class InvalidMoveException(PlayerException):
    def __init__(self, player_id: int, error_message: str, move: MoveType):
        super().__init__(player_id, error_message)
        self.details = move