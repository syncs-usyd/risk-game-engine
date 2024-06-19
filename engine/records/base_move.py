from pydantic import ValidationInfo, field_validator
from engine.records.base_record import BaseRecord

class BaseMove(BaseRecord):
    move_by_player: int

    @field_validator("move_by_player")
    @classmethod
    def _check_move_made_by_player(cls, v: int, info: ValidationInfo):
        player = info.context["player"] # type: ignore

        if not v == player:
            raise ValueError("You set 'move_by_player' to a player_id other than yourself.")
        
        return v
