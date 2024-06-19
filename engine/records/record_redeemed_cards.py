from pydantic import BaseModel


class RecordRedeemedCards(BaseModel):
    redeem_cards_move: int
    total_set_bonus: int
    matching_territory_bonus: int