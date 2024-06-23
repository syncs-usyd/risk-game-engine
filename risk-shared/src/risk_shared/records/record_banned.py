from typing import Any, Literal, Optional, Union, final
from risk_shared.output.ban_type import BanType
from risk_shared.records.base_record import BaseRecord
from risk_shared.records.types.move_type import MoveType

@final
class RecordBanned(BaseRecord):
    record_type: Literal["record_banned"] = "record_banned"
    player: int
    ban_type: BanType
    reason: str
    details: Optional[Union[list[Any], MoveType, Any]]