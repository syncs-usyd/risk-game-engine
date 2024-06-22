from typing import Literal, Union


BanType = Union[Literal["TIMEOUT"], Literal["CUMULATIVE_TIMEOUT"], Literal["BROKEN_PIPE"], Literal["INVALID_MESSAGE"], Literal["INVALID_MOVE"]]