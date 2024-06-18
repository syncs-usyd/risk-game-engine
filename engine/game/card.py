from typing import final
from engine.models.card_model import CardModel

@final
class Card(CardModel):

    @classmethod
    def factory(cls, territory_id: int, troop_count: int, troop_type: str) -> 'Card':
        return cls(territory_id=territory_id, occupier=None, troops_count=troop_count, troop_type=troop_type)