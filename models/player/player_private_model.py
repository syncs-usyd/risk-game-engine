from typing import Iterable
from models.card_model import CardModel
from models.player.player_public_model import PlayerPublicModel


class PlayerPrivateModel(PlayerPublicModel):
    cards: Iterable[CardModel]