from typing import Literal, Tuple, Union
from risk_helper.connection import Connection
from risk_helper.state import State
from risk_helper.state_mutator import StateMutator
from risk_shared.queries.query_attack import QueryAttack
from risk_shared.queries.query_claim_territory import QueryClaimTerritory
from risk_shared.queries.query_defend import QueryDefend
from risk_shared.queries.query_distribute_troops import QueryDistributeTroops
from risk_shared.queries.query_fortify import QueryFortify
from risk_shared.queries.query_place_initial_troop import QueryPlaceInitialTroop
from risk_shared.queries.query_redeem_cards import QueryRedeemCards
from risk_shared.queries.query_troops_after_attack import QueryTroopsAfterAttack
from risk_shared.queries.query_type import QueryType
from risk_shared.records.moves.move_attack import MoveAttack, MoveAttackDescription
from risk_shared.records.moves.move_claim_territory import MoveClaimTerritory
from risk_shared.records.moves.move_defend import MoveDefend
from risk_shared.records.moves.move_distribute_troops import MoveDistributeTroops
from risk_shared.records.moves.move_fortify import MoveFortify
from risk_shared.records.moves.move_place_initial_troop import MovePlaceInitialTroop
from risk_shared.records.moves.move_redeem_cards import MoveRedeemCards
from risk_shared.records.moves.move_troops_after_attack import MoveTroopsAfterAttack


class Game():

    def __init__(self):
        self.state = State()
        self.mutator = StateMutator(self.state)
        self.connection = Connection()


    def get_next_query(self) -> QueryType:
        query = self.connection.get_next_query()
        
        for i, record in query.update.items():
            self.mutator.commit(i, record)

        return query


    def move_attack(self, query: QueryAttack, move: Union[Literal["pass"], MoveAttackDescription]) -> None:
        self.connection.send_move(MoveAttack(
            move_by_player=self.state.me.player_id,
            move=move
        ))


    def move_claim_territory(self, query: QueryClaimTerritory, territory: int) -> None:
        self.connection.send_move(MoveClaimTerritory(
            move_by_player=self.state.me.player_id,
            territory=territory
        ))


    def move_defend(self, query: QueryDefend, defending_troops: int) -> None:
        self.connection.send_move(MoveDefend(
            move_by_player=self.state.me.player_id,
            move_attack_id=query.move_attack_id,
            defending_troops=defending_troops
        ))


    def move_distribute_troops(self, query: QueryDistributeTroops, distributions: dict[int, int]) -> None:
        self.connection.send_move(MoveDistributeTroops(
            move_by_player=self.state.me.player_id,
            distributions=distributions
        ))


    def move_fortify(self, query: QueryFortify, source_territory: int, target_territory: int, troop_count: int) -> None:
        self.connection.send_move(MoveFortify(
            move_by_player=self.state.me.player_id,
            source_territory=source_territory,
            target_territory=target_territory,
            troop_count=troop_count
        ))


    def move_place_initial_troop(self, query: QueryPlaceInitialTroop, territory:int) -> None:
        self.connection.send_move(MovePlaceInitialTroop(
            move_by_player=self.state.me.player_id,
            territory=territory
        ))


    def move_redeem_cards(self, query: QueryRedeemCards, sets: list[Tuple[int, int, int]] ) -> None:
        self.connection.send_move(MoveRedeemCards(
            move_by_player=self.state.me.player_id,
            cause=query.cause,
            sets=sets
        ))


    def move_troops_after_attack(self, query: QueryTroopsAfterAttack, troop_count: int) -> None:
        self.connection.send_move(MoveTroopsAfterAttack(
            move_by_player=self.state.me.player_id, 
            record_attack_id=query.record_attack_id, 
            troop_count=troop_count
        ))
