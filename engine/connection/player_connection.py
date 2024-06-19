from io import TextIOWrapper
import math
import random
from signal import SIGALRM, alarm, signal
from time import time
from typing import Callable, ParamSpec, Type, TypeVar, final

from pydantic import BaseModel, ValidationError

from engine.config.ioconfig import CORE_DIRECTORY, CUMULATIVE_TIMEOUT_SECONDS, MAX_CHARACTERS_READ, READ_CHUNK_SIZE, TIMEOUT_SECONDS
from engine.exceptions import BrokenPipeException, CumulativeTimeoutException, EngineException, InvalidResponseException, TimeoutException
from engine.game.state import State
from engine.queries.query_claim_territory import QueryClaimTerritory
from engine.queries.query_defend import QueryDefend
from engine.queries.query_place_initial_troop import QueryPlaceInitialTroop
from engine.queries.query_attack import QueryAttack
from engine.queries.query_distribute_troops import QueryDistributeTroops
from engine.queries.query_redeem_cards import QueryRedeemCards
from engine.queries.query_fortify import QueryFortifyTerritory
from engine.records.moves.move_claim_territory import MoveClaimTerritory
from engine.records.moves.move_claim_territory import MoveClaimTerritory
from engine.records.moves.move_defend import MoveDefend
from engine.records.moves.move_place_initial_troop import MovePlaceInitialTroop
from engine.records.moves.move_distribute_troops import MoveDistributeTroops
from engine.records.moves.move_redeem_cards import MoveRedeemCards
from engine.records.moves.move_fortify import MoveFortify
from engine.records.moves.move_attack import MoveAttack
from engine.records.record_turn_order import RecordTurnOrder

P = ParamSpec("P")
T1 = TypeVar("T1")
def handle_sigpipe(fn: Callable[P, T1]) -> Callable[P, T1]:
    """Decorator to trigger ban if the player closes the from_engine pipe.
    """

    def dfn(*args: P.args, **kwargs: P.kwargs) -> T1:
        self: 'PlayerConnection' = args[0] # type: ignore
        try:
            result = fn(*args, **kwargs)
        except BrokenPipeError:
            raise BrokenPipeException(self.player_id, "You closed 'from_engine.pipe'.")

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
            raise InvalidResponseException(self.player_id, "You sent an invalid message to the game engine: \n" + e.json(indent=2))

        return result
    
    return dfn
    

def time_limited(error_message: str = "You took too long to respond."):
    """Decorator to trigger ban if the player takes too long to respond.
    """

    def dfn1(fn: Callable[P, T1]):
        def dfn2(*args: P.args, **kwargs: P.kwargs) -> T1:
            self: 'PlayerConnection' = args[0]  # type: ignore
            def on_timeout_alarm(*_):
                raise TimeoutException(self.player_id, error_message)
            signal(SIGALRM, on_timeout_alarm)

            alarm(TIMEOUT_SECONDS)
            start = time()

            result = fn(*args, **kwargs)

            end = time()
            alarm(0) 

            self._cumulative_time += end - start
            if self._cumulative_time > CUMULATIVE_TIMEOUT_SECONDS:
                raise CumulativeTimeoutException(self.player_id, error_message)
            
            return result

        return dfn2
    
    return dfn1


T2 = TypeVar("T2", bound=BaseModel)
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


    def _send(self, data: str):
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
            raise InvalidResponseException(player_id=self.player_id, error_message="Malformed message size on message written to 'to_engine.pipe'.")
        
        if size > MAX_CHARACTERS_READ:
            raise InvalidResponseException(player_id=self.player_id, error_message=f"Message size too long for message written to 'to_engine.pipe', {size} > {MAX_CHARACTERS_READ}.")
        
        # Read message.
        buffer = bytearray()
        while len(buffer) < size:
            buffer.extend(bytearray(self._to_engine_pipe.read((size - len(buffer)) % READ_CHUNK_SIZE).encode()))

        return buffer.decode()


    @handle_invalid
    @handle_sigpipe
    @time_limited()
    def _query_move(self, query: BaseModel, response: Type[T2], state: State) -> T2:
        self._send(query.model_dump_json())

        _response = self._receive()
        return response.model_validate_json(_response, context={"state": state, "player": self.player_id})

    def _get_record_update_dict(self, state: State):
        if self._record_update_watermark >= len(state.match_history):
            raise RuntimeError("Record update watermark out of sync with state, did you try to send two queries without committing the first?")
        result = dict([(i, x) for i, x in enumerate(state.match_history[self._record_update_watermark:])])
        self._record_update_watermark = len(state.match_history)
        return result

    def query_claim_territory(self, state: State) -> MoveClaimTerritory:
        data = QueryClaimTerritory(you=state.players[self.player_id], update=self._get_record_update_dict(state)))
        return self._query_move(data, MoveClaimTerritory, state)


    def query_place_initial_troop(self, state: State) -> MovePlaceInitialTroop:
        data = QueryPlaceInitialTroop(you=state.players[self.player_id], update=self._get_record_update_dict(state))
        return self._query_move(data, MovePlaceInitialTroop, state)


    def query_attack(self, state: State) -> MoveAttack:
        data = QueryAttack(you=state.players[self.player_id], update=self._get_record_update_dict(state))
        return self._query_move(data, MoveAttack, state)


    def query_defend(self, state: State) -> MoveDefend:
        data = QueryDefend(you=state.players[self.player_id], update=self._get_record_update_dict(state))
        return self._query_move(data, MoveDefend, state)
        

    def query_distribute_troops(self, state: State) -> MoveDistributeTroops:
        data = QueryDistributeTroops(you=state.players[self.player_id], update=self._get_record_update_dict(state))
        return self._query_move(data, MoveDistributeTroops, state) 
    

    def query_redeem_cards(self, state: State) -> MoveRedeemCards:
        data = QueryRedeemCards(you=state.players[self.player_id], update=self._get_record_update_dict(state))
        return self._query_move(data, MoveRedeemCards, state) 
    

    def query_fortify(self, state: State) -> MoveFortify:
        data = QueryFortifyTerritory(you=state.players[self.player_id], update=self._get_record_update_dict(state))
        return self._query_move(data, MoveFortify, state) 


if __name__ == "__main__":
    state = State()
    connection = PlayerConnection(player_id=0)

    turn_order = [x for x in range(5)]
    random.shuffle(turn_order)
    record_turn_order = RecordTurnOrder(turn_order=turn_order)
    record_turn_order.commit(state)

    try:
        response = connection.query_claim_territory(state)
        response.commit(state)
        print(state.territories)
    except EngineException as e:
        raise e