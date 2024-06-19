from pydantic import BaseModel


class PlayerPublicModel(BaseModel):
    player_id: int
    troops_remaining: int
    alive: bool
    cards_held: int