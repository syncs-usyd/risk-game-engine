from typing import Sequence

from pydantic import BaseModel
from engine.models.card_model import CardModel


class PlayerModel(BaseModel):
    player_id: int
    troops_remaining: int
    alive: bool
    cards: Sequence[CardModel]
    must_place_territory_bonus: list[int]

    def get_public(self) -> 'PublicPlayerModel':
        return PublicPlayerModel(player_id=self.player_id, troops_remaining=self.troops_remaining, alive=self.alive, cards_count=len(self.cards))


class PublicPlayerModel(BaseModel):
    player_id: int
    troops_remaining: int
    alive: bool
    cards_count: int