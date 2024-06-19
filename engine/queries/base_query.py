from typing import Union
from pydantic import BaseModel, Field

from engine.models.player.player_model import PlayerModel
from engine.records.moves.move_attack import MoveAttack
from engine.records.moves.move_claim_territory import MoveClaimTerritory
from engine.records.moves.move_defend import MoveDefend
from engine.records.moves.move_fortify import MoveFortify
from engine.records.moves.move_place_initial_troop import MovePlaceInitialTroop
from engine.records.moves.move_redeem_cards import MoveRedeemCards
from engine.records.record_attack import RecordAttack
from engine.records.record_drew_card import PublicRecordDrewCard
from engine.records.record_player_eliminated import PublicRecordPlayerEliminated
from engine.records.record_redeemed_cards import RecordRedeemedCards
from engine.records.record_shuffled_cards import RecordShuffledCards
from engine.records.record_start_game import RecordStartGame
from engine.records.record_start_turn import RecordStartTurn
from engine.records.record_territory_conquered import RecordTerritoryConquered


class BaseQuery(BaseModel):
    query_type: str
    you: PlayerModel
    update: dict[int, Union[RecordAttack, PublicRecordDrewCard, PublicRecordPlayerEliminated,
                            RecordRedeemedCards, RecordShuffledCards, RecordStartGame, 
                            RecordStartTurn, RecordTerritoryConquered, MoveAttack, 
                            MoveClaimTerritory, MoveDefend, MoveFortify, 
                            MovePlaceInitialTroop, MoveRedeemCards]] = Field(discriminator="record_type")
