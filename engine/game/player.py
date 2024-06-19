

from typing import final
from engine.models.player.player_private_model import PlayerPrivateModel


@final
class Player(PlayerPrivateModel):

    @classmethod
    def factory(cls, player_id: int, initial_troops: int) -> 'Player':
        return cls(player_id=player_id, troops=initial_troops, alive=True, cards=[])
    
    def get_cards(self):
        return self.cards