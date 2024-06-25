from typing import Any, Optional
from risk_shared.queries.query_type import QueryType
from risk_shared.records.types.move_type import MoveType


class PlayerException(Exception):
    def __init__(self, player_id: int, error_message: str, details: Optional[Any]):
        super().__init__(error_message)
        self.player_id = player_id
        self.error_message = error_message
        self.details = details

class TimeoutException(PlayerException):
    def __init__(self, player_id: int, error_message: str, query: Optional[QueryType]):
        super().__init__(player_id, error_message, query)

class CumulativeTimeoutException(PlayerException):
    def __init__(self, player_id: int, error_message: str, query: Optional[QueryType]):
        super().__init__(player_id, error_message, query)

class BrokenPipeException(PlayerException):
    def __init__(self, player_id: int, error_message: str, query: Optional[QueryType]):
        super().__init__(player_id, error_message, query)

class InvalidMessageException(PlayerException):
    def __init__(self, player_id: int, error_message: str, details: Optional[list[Any]] = None):
        super().__init__(player_id, error_message, details)

class InvalidMoveException(PlayerException):
    def __init__(self, player_id: int, error_message: str, move: MoveType):
        super().__init__(player_id, error_message, move)