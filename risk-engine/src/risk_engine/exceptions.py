class PlayerException(Exception):
    def __init__(self, player_id, error_message: str):
        super().__init__(error_message)
        self.player_id = player_id
        self.error_message = error_message


class TimeoutException(PlayerException):
    pass

class CumulativeTimeoutException(PlayerException):
    pass

class BrokenPipeException(PlayerException):
    pass

class InvalidResponseException(PlayerException):
    pass