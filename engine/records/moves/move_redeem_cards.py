from typing import List, Tuple
from pydantic import BaseModel, ValidationInfo, field_validator

from engine.game.card import Card
from engine.game.state import State

class MoveRedeemCards(BaseModel):
    sets: list[Tuple[int, int, int]]

    @field_validator("sets")
    @classmethod
    def _check_redeem_player_cards(cls, sets: list[Tuple[int, int, int]], info: ValidationInfo):
        state: State = info.context["state"] # type: ignore
        player = info.context["player"] # type: ignore

        def check_card_set(card_set):
            for i in card_set:
                if i not in state.cards:
                    raise ValueError(f"You tried to redeem a nonexistant card with id {i}")
            cards: list[Card] = [state.cards[i] for i in card_set]

            unique_symbols = len(set(map(lambda x: x.symbol, cards)))
            if not (unique_symbols == 3 or unique_symbols == 1):
                raise ValueError(f"You tried to redeem a set of cards {cards[0].symbol}, {cards[1].symbol}, {cards[2].symbol}, which is not a set.")

        def check_owns_cards(cards):
            for card in cards:
                if card not in set(map(lambda x: x.card_id, state.players[player].cards)):
                    raise ValueError(f"You tried to redeem card {card}, which you don't possess.")

        def check_no_duplicates(cards):
            if len(set(cards)) != len(cards):
                raise ValueError(f"Your card sets contain duplicates of a single card.")

        all_cards = []
        for card_set in sets:
            check_card_set(card_set)
            all_cards.extend(card_set)

        check_owns_cards(all_cards)
        check_no_duplicates(all_cards) 
        
        return sets