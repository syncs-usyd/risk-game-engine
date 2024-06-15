from pydantic import BaseModel


class PlayerPublicModel(BaseModel):
    player_id: int
    troops: int
    alive: bool