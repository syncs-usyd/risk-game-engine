class EngineException(Exception):
    def __init__(self, player_id, error_message: str):
        super().__init__(error_message)
        self.player_id = player_id
        self.error_message = error_message


class TimeoutException(EngineException):
    pass

class CumulativeTimeoutException(EngineException):
    pass

class BrokenPipeException(EngineException):
    pass

class InvalidResponseException(EngineException):
    pass