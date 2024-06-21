
from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from engine.records.moves.move_attack import MoveAttack
    from engine.records.moves.move_claim_territory import MoveClaimTerritory
    from engine.records.moves.move_defend import MoveDefend
    from engine.records.moves.move_fortify import MoveFortify
    from engine.records.moves.move_place_initial_troop import MovePlaceInitialTroop
    from engine.records.moves.move_redeem_cards import MoveRedeemCards
    from engine.records.moves.move_troops_after_attack import MoveTroopsAfterAttack
    from engine.records.record_attack import RecordAttack
    from engine.records.record_banned import RecordBanned
    from engine.records.record_drew_card import PublicRecordDrewCard, RecordDrewCard
    from engine.records.record_player_eliminated import PublicRecordPlayerEliminated, RecordPlayerEliminated
    from engine.records.record_redeemed_cards import RecordRedeemedCards
    from engine.records.record_shuffled_cards import RecordShuffledCards
    from engine.records.record_start_game import RecordStartGame
    from engine.records.record_start_turn import RecordStartTurn
    from engine.records.record_territory_conquered import RecordTerritoryConquered
    from engine.records.record_winner import RecordWinner


RecordType = Union['RecordAttack', 'PublicRecordDrewCard', 'RecordDrewCard', 
                    'PublicRecordPlayerEliminated', 'RecordPlayerEliminated',
                    'RecordRedeemedCards', 'RecordShuffledCards', 'RecordStartGame', 
                    'RecordStartTurn', 'RecordTerritoryConquered', 'MoveTroopsAfterAttack',
                    'MoveAttack', 'MoveClaimTerritory', 'MoveDefend', 'MoveFortify', 
                    'MovePlaceInitialTroop', 'MoveRedeemCards', 'RecordBanned', 'RecordWinner']