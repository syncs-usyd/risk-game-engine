from collections import defaultdict
from typing import cast
from risk_engine.game.engine_state import EngineState
from risk_shared.models.card_model import CardModel
from risk_shared.queries.base_query import BaseQuery
from risk_shared.queries.query_defend import QueryDefend
from risk_shared.queries.query_distribute_troops import QueryDistributeTroops
from risk_shared.queries.query_redeem_cards import QueryRedeemCards
from risk_shared.queries.query_troops_after_attack import QueryTroopsAfterAttack
from risk_shared.records.base_move import BaseMove
from risk_shared.records.moves.move_attack import MoveAttack
from risk_shared.records.moves.move_attack_pass import MoveAttackPass
from risk_shared.records.moves.move_claim_territory import MoveClaimTerritory
from risk_shared.records.moves.move_defend import MoveDefend
from risk_shared.records.moves.move_distribute_troops import MoveDistributeTroops
from risk_shared.records.moves.move_fortify import MoveFortify
from risk_shared.records.moves.move_fortify_pass import MoveFortifyPass
from risk_shared.records.moves.move_place_initial_troop import MovePlaceInitialTroop
from risk_shared.records.moves.move_redeem_cards import MoveRedeemCards
from risk_shared.records.moves.move_troops_after_attack import MoveTroopsAfterAttack
from risk_shared.records.record_attack import RecordAttack
from risk_shared.records.types.move_type import MoveType


class MoveValidator():

    def __init__(self, state: EngineState):
        self.state = state

    def validate(self, record: MoveType, query: BaseQuery, player: int) -> None:
        self._validate_move(record, query, player)

        match record:
            case MoveAttack() as r:
                return self._validate_move_attack(r, query, player)
            case MoveAttackPass() as r:
                return self._validate_move_attack_pass(r, query, player)
            case MoveClaimTerritory() as r:
                return  self._validate_move_claim_territory(r, query, player)
            case MoveDefend() as r:
                return self._validate_move_defend(r, query, player)
            case MoveDistributeTroops() as r:
                return self._validate_move_distribute_troops(r, query, player)
            case MoveFortify() as r:
                return self._validate_move_fortify(r, query, player)
            case MoveFortifyPass() as r:
                return self._validate_move_fortify_pass(r, query, player)
            case MovePlaceInitialTroop() as r:
                return self._validate_move_place_initial_troop(r, query, player)
            case MoveRedeemCards() as r:
                return self._validate_move_redeem_cards(r, query, player)
            case MoveTroopsAfterAttack() as r:
                return self._validate_move_troops_after_attack(r, query, player)
            case _:
                raise NotImplementedError


    def _validate_move(self, r: BaseMove, query: BaseQuery, player: int) -> None:
        if not r.move_by_player == player:
            raise ValueError("You set 'move_by_player' to a player_id other than your own.")


    def _validate_move_attack(self, r: MoveAttack, query: BaseQuery, player: int) -> None:
        attacking_territory = r.attacking_territory
        defending_territory = r.defending_territory
        attacking_troops = r.attacking_troops

        if not attacking_territory in self.state.territories:
            raise ValueError(f"No territory exists with territory_id {attacking_territory}.")
        
        if not defending_territory in self.state.territories:
            raise ValueError(f"No territory exists with territory_id {defending_territory}.")
        
        if self.state.territories[attacking_territory].occupier != player:
            raise ValueError(f"You don't occupy this territory.")
        
        if self.state.territories[defending_territory].occupier == player:
            raise ValueError(f"You are attacking your own territory.")
        
        if not self.state.map.is_adjacent(defending_territory, attacking_territory):
            raise ValueError(f"{defending_territory} is not adjacent to {attacking_territory}.")
        
        if not 1 <= attacking_troops <= 3:
            raise ValueError(f"You must commit between 1 and 3 troops for the attack, you committed {attacking_troops}.")
        
        if attacking_troops > self.state.territories[attacking_territory].troops - 1:
            raise ValueError(f"You do not have enough troops, you tried to commit {attacking_troops} troops but only have {self.state.territories[attacking_territory].troops}. Remember 1 troop must remain on the attacking territory.")


    def _validate_move_attack_pass(self, r: MoveAttackPass, query: BaseQuery, player: int) -> None:
        pass


    def _validate_move_claim_territory(self, r: MoveClaimTerritory, query: BaseQuery, player: int) -> None:
        if not r.territory in self.state.territories:
            raise ValueError(f"You tried to claim a nonexistant territory with id {r.territory}.")
        
        if self.state.territories[r.territory].occupier != None:
            raise ValueError(f"You tried to claim a territory that is already claimed.")  


    def _validate_move_defend(self, r: MoveDefend, query: BaseQuery, player: int) -> None:
        query = cast(QueryDefend, query)
        if r.move_attack_id != query.move_attack_id:
            raise ValueError(f"You have to defend the attack with record id {query.move_attack_id}.")

        move_attack_obj = cast(MoveAttack, self.state.recording[r.move_attack_id])
        
        defending_territory = move_attack_obj.defending_territory
        if self.state.territories[defending_territory].occupier != r.move_by_player:
            raise RuntimeError("Wrong player is defending.")

        if not 1 <= r.defending_troops <= 2:
            raise ValueError(f"You must commit 1 or 2 troops for the defence.")
        if self.state.territories[defending_territory].troops < r.defending_troops:
            raise ValueError(f"You tried to defend with more troops then you had occupying the defending territory.")


    def _validate_move_distribute_troops(self, r: MoveDistributeTroops, query: BaseQuery, player: int) -> None:
        query = cast(QueryDistributeTroops, query)
        for territory in r.distributions:
            if not territory in self.state.territories:
                raise ValueError(f"You tried to distribute troops to a nonexistant territory with id {territory}.")
            
            if self.state.territories[territory].occupier != player:
                raise ValueError(f"You don't occupy the territory with id {territory}.")  
            
        if sum(r.distributions.values()) != self.state.players[player].troops_remaining:
            raise ValueError(f"You must distribute exactly your remaining {self.state.players[player].troops_remaining} troops.")
        
        if r.cause != query.cause:
            raise ValueError(f"You tried to change the cause of this move from {query.cause}.")

        matching_territories = self.state.players[player].must_place_territory_bonus
        if len(matching_territories) > 0:
            for territory in matching_territories:
                if r.distributions[territory] >= 2:
                    break
            else:
                raise ValueError(f"You must distribute your matching territory bonus to a matching territory from your previous card redemption, at least 2 troops must be placed on a matching territory.\n Your matching territories are {matching_territories}.")


    def _validate_move_fortify(self, r: MoveFortify, query: BaseQuery, player: int) -> None:
        if not r.source_territory in self.state.territories:
            raise ValueError(f"Your source territory with id {r.source_territory} does not exist.")

        if not r.target_territory in self.state.territories:
            raise ValueError(f"Your target territory with id {r.source_territory} does not exist.")
        
        if self.state.territories[r.source_territory].occupier != player:
            raise ValueError(f"You don't occupy the source territory.")

        if self.state.territories[r.target_territory].occupier != player:
            raise ValueError(f"You don't occupy the target territory.")
        
        # The player can pass their turn by moving zero troops from one territory to itself.
        if r.troop_count == 0 and r.source_territory == r.target_territory:
            return

        if not self.state.map.is_adjacent(r.source_territory, r.target_territory):
            raise ValueError(f"Your target territory {r.target_territory} is not adjacent to your source territory {r.source_territory}.")
        
        if not 0 <= r.troop_count <= self.state.territories[r.source_territory].troops - 1:
            raise ValueError(f"You tried to move {r.troop_count} troops, you must move between zero and the number of troops in the source territory, subtracting one troop which must be left behind.")


    def _validate_move_fortify_pass(self, r: MoveFortifyPass, query: BaseQuery, player: int) -> None:
        pass


    def _validate_move_place_initial_troop(self, r: MovePlaceInitialTroop, query: BaseQuery, player: int) -> None:
        if not r.territory in self.state.territories:
            raise ValueError(f"You tried to claim a nonexistant territory with id {r.territory}.")
        
        if self.state.territories[r.territory].occupier != player:
            raise ValueError(f"You don't occupy this territory.")  


    def _validate_move_redeem_cards(self, r: MoveRedeemCards, query: BaseQuery, player: int) -> None:
        query = cast(QueryRedeemCards, query)
        if r.cause != query.cause:
            raise ValueError(f"You tried to change the cause of this move from {query.cause}.")

        def check_card_set(card_set):
            for i in card_set:
                if i not in self.state.cards:
                    raise ValueError(f"You tried to redeem a nonexistant card with id {i}")
            cards: list[CardModel] = [self.state.cards[i] for i in card_set]

            cards_by_symbol = defaultdict(lambda: 0)
            for card in cards:
                cards_by_symbol[card.symbol] += 1

            is_matching_set = len(cards_by_symbol) == 1 and "Wildcard" not in cards_by_symbol
            is_one_of_each_set = len(cards_by_symbol) == 3 and "Wildcard" not in cards_by_symbol
            is_wildcard_set = "Wildcard" in cards_by_symbol
            if not (is_matching_set or is_one_of_each_set or is_wildcard_set):
                raise ValueError(f"You tried to redeem a set of cards {cards[0].symbol}, {cards[1].symbol}, {cards[2].symbol}, which is not a set.")

        def check_owns_cards(cards):
            for card in cards:
                if card not in set(map(lambda x: x.card_id, self.state.players[player].cards)):
                    raise ValueError(f"You tried to redeem card {card}, which you don't possess.")

        def check_no_duplicates(cards):
            if len(set(cards)) != len(cards):
                raise ValueError(f"Your card sets contain duplicates of a single card.")

        all_cards = []
        for card_set in r.sets:
            check_card_set(card_set)
            all_cards.extend(card_set)

        check_owns_cards(all_cards)
        check_no_duplicates(all_cards) 
        
        cards_held_after_redeeming = len(set(map(lambda x: x.card_id, self.state.players[player].cards)) - set(all_cards))
        if cards_held_after_redeeming >= 5:
            raise ValueError(f"You need to redeem more cards, you must have less than 5 cards remaining after redeeming.")
        
        if r.cause == "player_eliminated" and cards_held_after_redeeming < 2:
            raise ValueError(f"You must stop redeeming cards once you have less than 5 cards remaining if you are redeeming cards after killing a player.")


    def _validate_move_troops_after_attack(self, r: MoveTroopsAfterAttack, query: BaseQuery, player: int) -> None:
        query = cast(QueryTroopsAfterAttack, query)
        if r.record_attack_id != query.record_attack_id:
            raise ValueError(f"You must move troops for the attack record with id {query.record_attack_id}.")

        record_attack = cast(RecordAttack, self.state.recording[r.record_attack_id])

        move_attack_id = record_attack.move_attack_id
        move_attack = cast(MoveAttack, self.state.recording[move_attack_id])

        minimum_troops_moved = move_attack.attacking_troops - record_attack.attacking_troops_lost

        if not minimum_troops_moved <= r.troop_count:
            raise ValueError("You must move troops from the attacking territory to the defending territory after a successful attack, depending on how many troops were committed and how many died.")
        
        if not r.troop_count <= self.state.territories[move_attack.attacking_territory].troops - 1:
            raise ValueError(f"You tried to move too many troops from territory {move_attack.attacking_territory}.")


