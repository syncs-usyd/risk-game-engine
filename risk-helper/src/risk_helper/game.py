from typing import Tuple
from risk_helper.connection import Connection
from risk_helper.client_state import ClientState
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
from risk_shared.records.types.move_type import MoveType


class Game():

    def __init__(self):
        self.state = ClientState()
        self.mutator = StateMutator(self.state)
        self.connection = Connection()


    def get_next_query(self) -> QueryType:
        query = self.connection.get_next_query()

        new_records_mark = len(self.state.recording)
        for i, record in query.update.items():
            self.mutator.commit(i, record)
        self.state.new_records = new_records_mark

        return query
    

    def send_move(self, move: MoveType) -> None:
        self.connection.send_move(move)


    def move_attack(self, query: QueryAttack, attacking_territory: int, defending_territory: int, attacking_troops: int) -> MoveAttack:
        return MoveAttack(
            move_by_player=self.state.me.player_id,
            attacking_territory=attacking_territory,
            defending_territory=defending_territory,
            attacking_troops=attacking_troops
        )
    

    def move_attack_pass(self, query: QueryAttack) -> MoveAttackPass:
        return MoveAttackPass(move_by_player=self.state.me.player_id)


    def move_claim_territory(self, query: QueryClaimTerritory, territory: int) -> MoveClaimTerritory:
        return MoveClaimTerritory(
            move_by_player=self.state.me.player_id,
            territory=territory
        )


    def move_defend(self, query: QueryDefend, defending_troops: int) -> MoveDefend:
        return MoveDefend(
            move_by_player=self.state.me.player_id,
            move_attack_id=query.move_attack_id,
            defending_troops=defending_troops
        )


    def move_distribute_troops(self, query: QueryDistributeTroops, distributions: dict[int, int]) -> MoveDistributeTroops:
        distributions = dict([(x, y) for x, y in distributions.items() if y > 0])
        
        return MoveDistributeTroops(
            move_by_player=self.state.me.player_id,
            cause=query.cause,
            distributions=distributions
        )


    def move_fortify(self, query: QueryFortify, source_territory: int, target_territory: int, troop_count: int) -> MoveFortify:
        return MoveFortify(
            move_by_player=self.state.me.player_id,
            source_territory=source_territory,
            target_territory=target_territory,
            troop_count=troop_count
        )
    

    def move_fortify_pass(self, query: QueryFortify) -> MoveFortifyPass:
        return MoveFortifyPass(
            move_by_player=self.state.me.player_id,
        )



    def move_place_initial_troop(self, query: QueryPlaceInitialTroop, territory:int) -> MovePlaceInitialTroop:
        return MovePlaceInitialTroop(
            move_by_player=self.state.me.player_id,
            territory=territory
        )


    def move_redeem_cards(self, query: QueryRedeemCards, sets: list[Tuple[int, int, int]] ) -> MoveRedeemCards:
        return MoveRedeemCards(
            move_by_player=self.state.me.player_id,
            cause=query.cause,
            sets=sets
        )


    def move_troops_after_attack(self, query: QueryTroopsAfterAttack, troop_count: int) -> MoveTroopsAfterAttack:
        return MoveTroopsAfterAttack(
            move_by_player=self.state.me.player_id, 
            record_attack_id=query.record_attack_id, 
            troop_count=troop_count
        )
