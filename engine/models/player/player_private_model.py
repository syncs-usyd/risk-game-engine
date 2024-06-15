from typing import Iterable
from engine.models.card_model import CardModel
from engine.models.player.player_public_model import PlayerPublicModel


class PlayerPrivateModel(PlayerPublicModel):
    cards: Iterable[CardModel]