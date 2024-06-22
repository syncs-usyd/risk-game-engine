
from typing import Union

from risk_shared.records.record_cancelled import RecordCancelled
from risk_shared.records.types.move_type import MoveType
from risk_shared.records.record_attack import RecordAttack
from risk_shared.records.record_banned import RecordBanned
from risk_shared.records.record_drew_card import PublicRecordDrewCard, RecordDrewCard
from risk_shared.records.record_player_eliminated import PublicRecordPlayerEliminated, RecordPlayerEliminated
from risk_shared.records.record_redeemed_cards import RecordRedeemedCards
from risk_shared.records.record_shuffled_cards import RecordShuffledCards
from risk_shared.records.record_start_game import PublicRecordStartGame, RecordStartGame
from risk_shared.records.record_start_turn import RecordStartTurn
from risk_shared.records.record_territory_conquered import RecordTerritoryConquered
from risk_shared.records.record_winner import RecordWinner


RecordType = Union[RecordAttack, PublicRecordDrewCard, RecordDrewCard, 
                    PublicRecordPlayerEliminated, RecordPlayerEliminated,
                    RecordRedeemedCards, RecordShuffledCards, RecordStartGame, 
                    PublicRecordStartGame, RecordStartTurn, RecordTerritoryConquered, 
                    RecordBanned, RecordCancelled, RecordWinner, MoveType]