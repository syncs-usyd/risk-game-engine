from pydantic import ValidationInfo, field_validator
from engine.records.base_record import BaseRecord


class BaseMove(BaseRecord):
    made_move: int

    @field_validator("made_move")
    @classmethod
    def _check_made_move(cls, v: int, info: ValidationInfo)
        player = info.context["player"] # type: ignore

        if not v == player:
            raise ValueError("You set 'made_move' to a player_id other than yourself.")
        
        return v