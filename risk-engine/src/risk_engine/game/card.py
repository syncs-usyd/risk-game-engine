from typing import Optional, final
from risk_shared.models.card_model import CardModel

@final
class Card(CardModel):

    @classmethod
    def factory(cls, card_id: int, territory_id: Optional[int], symbol) -> 'Card':
        return cls(card_id=card_id, territory_id=territory_id, symbol=symbol)