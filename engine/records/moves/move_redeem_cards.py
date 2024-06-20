from typing import Literal, Tuple, TypeGuard, Union, final
from pydantic import ValidationInfo, field_validator, model_validator

from engine.game.card import Card
from engine.game.state import State
from engine.queries.query_redeem_cards import QueryRedeemCards
from engine.records.base_move import BaseMove
from engine.records.record_redeemed_cards import RecordRedeemedCards

@final
class MoveRedeemCards(BaseMove):
    record_type: Literal["move_redeem_cards"] = "move_redeem_cards"
    sets: list[Tuple[int, int, int]]
    cause: Union[Literal["turn_started"], Literal["player_eliminated"]]

    @model_validator(mode="after")
    def _check_redeem_player_cards(self, info: ValidationInfo):
        state: State = info.context["state"] # type: ignore
        player: int = info.context["player"] # type: ignore
        query: QueryRedeemCards = info.context["query"] # type: ignore

        if self.cause != query.cause:
            raise ValueError(f"You tried to change the cause of this move from {query.cause}.")

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
        for card_set in self.sets:
            check_card_set(card_set)
            all_cards.extend(card_set)

        check_owns_cards(all_cards)
        check_no_duplicates(all_cards) 
        
        cards_held_after_redeeming = len(set(map(lambda x: x.card_id, state.players[player].cards)) - set(all_cards))
        if cards_held_after_redeeming >= 5:
            raise ValueError(f"You need to redeem more cards, you must have less than 5 cards remaining after redeeming.")
        
        if self.cause == "player_eliminated" and cards_held_after_redeeming < 2:
            raise ValueError("You must stop redeeming cards once you have less than 5 cards remaining if you are redeeming cards after killing a player.")

        return self


    def get_public_record(self, player_id: int):
        return self


    def commit(self, state: State) -> None:
        state.match_history.append(self)

        def calculate_set_bonus(x: int):
            fixed_values = [4, 6, 8, 10, 12, 15]
            if x < len(fixed_values):
                return fixed_values[x]
            
            return 15 + (x - len(fixed_values) + 1) * 5

        # Give the set bonus for each set redeemed.
        total_set_bonus = 0
        for _ in range(len(self.sets)):
            total_set_bonus += calculate_set_bonus(state.card_sets_redeemed)
            state.card_sets_redeemed += 1

        # Give the matching territory bonus if applicable.
        all_cards: list[int] = []
        for card_set in self.sets:
            all_cards.extend(card_set)

        def remove_none(x) -> TypeGuard[int]:
            return x != None
        
        matching_territories = set(filter(remove_none, [state.cards[card].territory_id for card in all_cards])) & set(map(lambda x: x.territory_id, filter(lambda x: x.occupier == self.move_by_player, state.territories.values())))
        matching_territory_bonus = 2 if len(matching_territories) > 0 else 0

        # Modify the player.
        state.players[self.move_by_player].troops_remaining += total_set_bonus + matching_territory_bonus
        state.players[self.move_by_player].must_place_territory_bonus = list(matching_territories)

        # Place the redeemed cards in the discarded deck.
        state.discarded_deck.extend([state.cards[i] for i in all_cards])
        
        # Emit a RecordRedeemedCards.
        record = RecordRedeemedCards(redeem_cards_move=len(state.match_history) - 1, total_set_bonus=total_set_bonus, matching_territory_bonus=matching_territory_bonus)
        record.commit(state)




        

