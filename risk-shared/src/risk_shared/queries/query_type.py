from typing import Union

from risk_shared.queries.query_attack import QueryAttack
from risk_shared.queries.query_claim_territory import QueryClaimTerritory
from risk_shared.queries.query_defend import QueryDefend
from risk_shared.queries.query_distribute_troops import QueryDistributeTroops
from risk_shared.queries.query_fortify import QueryFortify
from risk_shared.queries.query_place_initial_troop import QueryPlaceInitialTroop
from risk_shared.queries.query_redeem_cards import QueryRedeemCards
from risk_shared.queries.query_troops_after_attack import QueryTroopsAfterAttack


QueryType = Union[QueryAttack, QueryClaimTerritory, QueryDefend, 
                  QueryDistributeTroops, QueryFortify, QueryPlaceInitialTroop, 
                  QueryRedeemCards, QueryTroopsAfterAttack]