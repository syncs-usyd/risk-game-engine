from io import TextIOWrapper
import itertools
import json
import math
import random
from signal import SIGALRM, alarm, signal
from time import time
from typing import Callable, Literal, Optional, ParamSpec, Type, TypeVar, Union, final

from risk_engine.censoring.censor_record import CensorRecord
from risk_engine.game.state_mutator import StateMutator
from risk_engine.validation.move_validator import MoveValidator
from pydantic import TypeAdapter, ValidationError

from risk_engine.config.ioconfig import CORE_DIRECTORY, CUMULATIVE_TIMEOUT_SECONDS, MAX_CHARACTERS_READ, READ_CHUNK_SIZE, TIMEOUT_SECONDS
from risk_engine.exceptions import BrokenPipeException, CumulativeTimeoutException, InvalidMoveException, PlayerException, InvalidMessageException, TimeoutException
from risk_engine.game.engine_state import EngineState
from risk_shared.models.player_model import PlayerModel
from risk_shared.queries.query_type import QueryType
from risk_shared.records.moves.move_attack_pass import MoveAttackPass
from risk_shared.records.moves.move_fortify_pass import MoveFortifyPass
from risk_shared.records.moves.move_troops_after_attack import MoveTroopsAfterAttack
from risk_shared.records.types.move_type import MoveType
from risk_shared.queries.base_query import BaseQuery
from risk_shared.queries.query_claim_territory import QueryClaimTerritory
from risk_shared.queries.query_defend import QueryDefend
from risk_shared.queries.query_place_initial_troop import QueryPlaceInitialTroop
from risk_shared.queries.query_attack import QueryAttack
from risk_shared.queries.query_distribute_troops import QueryDistributeTroops
from risk_shared.queries.query_redeem_cards import QueryRedeemCards
from risk_shared.queries.query_fortify import QueryFortify
from risk_shared.queries.query_troops_after_attack import QueryTroopsAfterAttack
from risk_shared.records.moves.move_claim_territory import MoveClaimTerritory
from risk_shared.records.moves.move_claim_territory import MoveClaimTerritory
from risk_shared.records.moves.move_defend import MoveDefend
from risk_shared.records.moves.move_place_initial_troop import MovePlaceInitialTroop
from risk_shared.records.moves.move_distribute_troops import MoveDistributeTroops
from risk_shared.records.moves.move_redeem_cards import MoveRedeemCards
from risk_shared.records.moves.move_fortify import MoveFortify
from risk_shared.records.moves.move_attack import MoveAttack
from risk_shared.records.record_start_game import RecordStartGame

# Performance boost on deserializing unions.
cached_type_adapters: dict[frozenset[str], TypeAdapter] = {}


class InvalidMoveError(ValueError):
    def __init__(self, message: str, move: MoveType):
        super().__init__(message)
        self.invalid_move = move


P = ParamSpec("P")
T1 = TypeVar("T1")
def handle_sigpipe(fn: Callable[P, T1]) -> Callable[P, T1]:
    """Decorator to trigger ban if the player closes the from_engine pipe.
    """

    def dfn(*args: P.args, **kwargs: P.kwargs) -> T1:
        self: 'PlayerConnection' = args[0] # type: ignore
        query: Optional[QueryType] = None
        if len(args) >= 2 and isinstance(args[1], BaseQuery):
                query = args[1]   # type: ignore
        try:
            result = fn(*args, **kwargs)
        except BrokenPipeError:
            raise BrokenPipeException(self.player_id, "You closed 'from_engine.pipe'.", query)

        return result
    
    return dfn


def handle_invalid(fn: Callable[P, T1]) -> Callable[P, T1]:
    """Decorator to trigger ban if the player sends an invalid, but syntactically correct message.
    """

    def dfn(*args: P.args, **kwargs: P.kwargs) -> T1:
        self: 'PlayerConnection' = args[0] # type: ignore
        try:
            result = fn(*args, **kwargs)
        except ValidationError as e:
            raise InvalidMessageException(self.player_id, "You sent an invalid message to the game engine.", json.loads(e.json()))
        except InvalidMoveError as e:
            raise InvalidMoveException(self.player_id, str(e), e.invalid_move)
        return result
    
    return dfn
    

def time_limited(error_message: str = "You took too long to respond."):
    """Decorator to trigger ban if the player takes too long to respond.
    """

    def dfn1(fn: Callable[P, T1]):
        def dfn2(*args: P.args, **kwargs: P.kwargs) -> T1:
            self: 'PlayerConnection' = args[0]  # type: ignore
            query: Optional[QueryType] = None
            if len(args) >= 2 and isinstance(args[1], BaseQuery):
                query = args[1]   # type: ignore

            def on_timeout_alarm(*_):
                raise TimeoutException(self.player_id, error_message, query)
            signal(SIGALRM, on_timeout_alarm)

            alarm(TIMEOUT_SECONDS)
            start = time()

            result = fn(*args, **kwargs)

            end = time()
            alarm(0) 

            self._cumulative_time += end - start
            if self._cumulative_time > CUMULATIVE_TIMEOUT_SECONDS:
                raise CumulativeTimeoutException(self.player_id, error_message, query)
            
            return result

        return dfn2
    
    return dfn1


T2 = TypeVar("T2", bound=MoveType)
T3 = TypeVar("T3", bound=MoveType)
@final
class PlayerConnection():

    def __init__(self, player_id: int):
        self.player_id: int = player_id
        self._to_engine_pipe: TextIOWrapper
        self._from_engine_pipe: TextIOWrapper
        self._cumulative_time: float = 0
        self._record_update_watermark: int = 0

        self._open_pipes()


    @time_limited("You didn't open 'to_engine' for writing or 'from_engine.pipe' for reading in time.")
    def _open_pipes(self):
        self._to_engine_pipe = open(f"{CORE_DIRECTORY}/submission{self.player_id}/io/to_engine.pipe", "r")
        self._from_engine_pipe = open(f"{CORE_DIRECTORY}/submission{self.player_id}/io/from_engine.pipe", "w")


    def _send(self, data: str) -> None:
        self._from_engine_pipe.write(str(len(data)) + ",")
        self._from_engine_pipe.write(data)
        self._from_engine_pipe.flush()


    def _receive(self) -> str:

        # Read size of message.
        buffer = bytearray()
        while len(buffer) < math.floor(math.log10(MAX_CHARACTERS_READ)) + 1 and (len(buffer) == 0 or buffer[-1] != ord(",")):
            buffer.extend(self._to_engine_pipe.read(1).encode())

        if buffer[-1] == ord(","):
            size = int(buffer[0:-1].decode())
        else:
            raise InvalidMessageException(player_id=self.player_id, error_message=f"You send a message with a malformed message size.")
        
        if size > MAX_CHARACTERS_READ:
            raise InvalidMessageException(player_id=self.player_id, error_message=f"You send a message that was too long, {size} > {MAX_CHARACTERS_READ} maximum.")
        
        # Read message.
        buffer = bytearray()
        while len(buffer) < size:
            buffer.extend(bytearray(self._to_engine_pipe.read(min((size - len(buffer)), READ_CHUNK_SIZE)).encode()))

        return buffer.decode()


    @handle_invalid
    @handle_sigpipe
    @time_limited()
    def _query_move(self, query: QueryType, response_type: Type[T2], validator: MoveValidator) -> T2:
        self._send(query.model_dump_json())

        move = response_type.model_validate_json(self._receive())
        try:
            validator.validate(move, query, self.player_id)
        except ValueError as e:
            raise InvalidMoveError(str(e), move)
        return move
    

    @handle_invalid
    @handle_sigpipe
    @time_limited()
    def _query_move_union(self, query: QueryType, response_type_1: Type[T2], response_type_2: Type[T3], validator: MoveValidator) -> Union[T2, T3]:
        self._send(query.model_dump_json())

        types = frozenset([response_type_1.__name__, response_type_2.__name__])
        if types in cached_type_adapters:
            adapter = cached_type_adapters[types]
        else:
            cached_type_adapters[types] = TypeAdapter(Union[response_type_1, response_type_2])
            adapter = cached_type_adapters[types]
        
        move = adapter.validate_json(self._receive())
        try:
            validator.validate(move, query, self.player_id)
        except ValueError as e:
            raise InvalidMoveError(str(e), move)
        return move


    def _get_record_update_dict(self, state: EngineState, censor: CensorRecord):
        if self._record_update_watermark >= len(state.recording):
            raise RuntimeError("Record update watermark out of sync with state, did you try to send two queries without committing the first?")
        result = dict([(i, censor.censor(x, self.player_id)) for i, x in itertools.islice(enumerate(state.recording), self._record_update_watermark, None)])
        self._record_update_watermark = len(state.recording)
        return result


    def query_claim_territory(self, state: EngineState, validator: MoveValidator, censor: CensorRecord) -> MoveClaimTerritory:
        query = QueryClaimTerritory(update=self._get_record_update_dict(state, censor))
        return self._query_move(query, MoveClaimTerritory, validator)


    def query_place_initial_troop(self, state: EngineState, validator: MoveValidator, censor: CensorRecord) -> MovePlaceInitialTroop:
        query = QueryPlaceInitialTroop(update=self._get_record_update_dict(state, censor))
        return self._query_move(query, MovePlaceInitialTroop, validator)


    def query_attack(self, state: EngineState, validator: MoveValidator, censor: CensorRecord) -> Union[MoveAttack, MoveAttackPass]:
        query = QueryAttack(update=self._get_record_update_dict(state, censor))
        return self._query_move_union(query, MoveAttack, MoveAttackPass, validator)


    def query_defend(self, state: EngineState, validator: MoveValidator, censor: CensorRecord, move_attack_id: int) -> MoveDefend:
        query = QueryDefend(move_attack_id=move_attack_id, update=self._get_record_update_dict(state, censor))
        return self._query_move(query, MoveDefend, validator)
    

    def query_troops_after_attack(self, state: EngineState, validator: MoveValidator, censor: CensorRecord, record_attack_id: int) -> MoveTroopsAfterAttack:
        query = QueryTroopsAfterAttack(record_attack_id=record_attack_id, update=self._get_record_update_dict(state, censor))
        return self._query_move(query, MoveTroopsAfterAttack, validator)
        

    def query_distribute_troops(self, state: EngineState, validator: MoveValidator, censor: CensorRecord, cause: Union[Literal["turn_started"], Literal["player_eliminated"]]) -> MoveDistributeTroops:
        query = QueryDistributeTroops(cause=cause, update=self._get_record_update_dict(state, censor))
        return self._query_move(query, MoveDistributeTroops, validator) 
    

    def query_redeem_cards(self, state: EngineState, validator: MoveValidator, censor: CensorRecord, cause: Union[Literal["turn_started"], Literal["player_eliminated"]]) -> MoveRedeemCards:
        query = QueryRedeemCards(cause=cause, update=self._get_record_update_dict(state, censor))
        return self._query_move(query, MoveRedeemCards, validator) 
    

    def query_fortify(self, state: EngineState, validator: MoveValidator, censor: CensorRecord) -> Union[MoveFortify, MoveFortifyPass]:
        query = QueryFortify(update=self._get_record_update_dict(state, censor))
        return self._query_move_union(query, MoveFortify, MoveFortifyPass, validator) 


if __name__ == "__main__":
    state = EngineState()
    mutator = StateMutator(state)
    validator = MoveValidator(state)
    censor = CensorRecord(state)
    connection = PlayerConnection(player_id=0)
    players = [PlayerModel(player_id=0, team_id=0, troops_remaining=25, alive=True, cards=[], must_place_territory_bonus=[])]

    turn_order = [x for x in range(5)]
    random.shuffle(turn_order)
    record_turn_order = RecordStartGame(turn_order=turn_order, players=players)
    mutator.commit(record_turn_order)

    try:
        response = connection.query_claim_territory(state, validator, censor)
        mutator.commit(response)
        print(state.territories)
    except PlayerException as e:
        raise e