

from typing import cast
from risk_engine.game.engine_state import EngineState
from risk_shared.records.moves.move_attack import MoveAttack
from risk_shared.records.record_attack import RecordAttack
from risk_shared.records.record_drew_card import PublicRecordDrewCard, RecordDrewCard
from risk_shared.records.record_player_eliminated import PublicRecordPlayerEliminated, RecordPlayerEliminated
from risk_shared.records.record_start_game import PublicRecordStartGame, RecordStartGame
from risk_shared.records.types.record_type import RecordType


class CensorRecord():

    def __init__(self, state: EngineState):
        self.state = state

    def censor(self, record: RecordType, player_id: int) -> RecordType:
        
        match record:
            case RecordDrewCard() as r:
                if r.player == player_id:
                    return r
                return PublicRecordDrewCard(player=r.player)
            
            case RecordPlayerEliminated() as r:
                record_attack = cast(RecordAttack, self.state.recording[r.record_attack_id])
                move_attack = cast(MoveAttack, self.state.recording[record_attack.move_attack_id])
                if move_attack.move_by_player == player_id:
                    return r
                return PublicRecordPlayerEliminated(player=r.player, record_attack_id=r.record_attack_id, cards_surrendered_count=len(r.cards_surrendered))

            case RecordStartGame() as r:
                return PublicRecordStartGame(turn_order=r.turn_order, players=[player.get_public() for player in r.players], you=filter(lambda x: x.player_id == player_id, r.players).__next__())
    

        return record