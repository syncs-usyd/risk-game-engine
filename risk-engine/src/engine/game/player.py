

from typing import final

from risk_shared.models.player_model import PlayerModel


@final
class Player(PlayerModel):

    @classmethod
    def factory(cls, player_id: int, initial_troops: int) -> 'Player':
        return cls(player_id=player_id, troops_remaining=initial_troops, alive=True, cards=[], must_place_territory_bonus=[])
    
    def get_cards(self):
        return self.cards
    