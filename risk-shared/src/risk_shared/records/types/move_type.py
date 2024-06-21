from typing import Union

from risk_shared.records.moves.move_attack import MoveAttack
from risk_shared.records.moves.move_claim_territory import MoveClaimTerritory
from risk_shared.records.moves.move_defend import MoveDefend
from risk_shared.records.moves.move_distribute_troops import MoveDistributeTroops
from risk_shared.records.moves.move_fortify import MoveFortify
from risk_shared.records.moves.move_place_initial_troop import MovePlaceInitialTroop
from risk_shared.records.moves.move_redeem_cards import MoveRedeemCards
from risk_shared.records.moves.move_troops_after_attack import MoveTroopsAfterAttack


MoveType = Union[MoveTroopsAfterAttack, MoveAttack, MoveClaimTerritory, MoveDefend, 
                 MoveDistributeTroops, MoveFortify, MovePlaceInitialTroop, MoveRedeemCards]