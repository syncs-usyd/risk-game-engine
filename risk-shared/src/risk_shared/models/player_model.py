from pydantic import BaseModel
from risk_shared.models.card_model import CardModel


class PlayerModel(BaseModel):
    player_id: int
    team_id: int
    troops_remaining: int
    alive: bool
    cards: list[CardModel]
    must_place_territory_bonus: list[int]

    def get_public(self) -> 'PublicPlayerModel':
        return PublicPlayerModel(player_id=self.player_id, troops_remaining=self.troops_remaining, alive=self.alive, card_count=len(self.cards), must_place_territory_bonus=self.must_place_territory_bonus)


class PublicPlayerModel(BaseModel):
    player_id: int
    troops_remaining: int
    alive: bool
    card_count: int
    must_place_territory_bonus: list[int]