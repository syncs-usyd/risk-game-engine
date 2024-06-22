from risk_shared.records.types.move_type import MoveType


class PlayerException(Exception):
    def __init__(self, player_id: int, error_message: str):
        super().__init__(error_message)
        self.player_id = player_id
        self.error_message = error_message


class TimeoutException(PlayerException):
    pass

class CumulativeTimeoutException(PlayerException):
    pass

class BrokenPipeException(PlayerException):
    pass

class InvalidMessageException(PlayerException):
    pass

class InvalidMoveException(PlayerException):
    def __init__(self, player_id: int, error_message: str, move: MoveType):
        super().__init__(player_id, error_message)
        self.invalid_move = move