from io import TextIOWrapper
import math
from signal import SIGALRM, alarm, signal
from time import time
from typing import Callable, ParamSpec, TypeVar, final

from pydantic import ValidationError

from engine.config.ioconfig import CORE_DIRECTORY, CUMULATIVE_TIMEOUT_SECONDS, MAX_CHARACTERS_READ, READ_CHUNK_SIZE, TIMEOUT_SECONDS
from engine.exceptions import BrokenPipeException, CumulativeTimeoutException, EngineException, InvalidResponseException, TimeoutException
from engine.game.state import State
from engine.queries.query_claim_territory import QueryClaimTerritory
from engine.queries.query_place_initial_troop import QueryPlaceInitialTroop
from engine.queries.query_place_player_troop import QueryPlacePlayerTroop
from engine.queries.query_redeem_card_decision import QueryRedeemCardDecision
from engine.queries.query_redeem_player_cards import QueryRedeemPlayerCards
from engine.responses.response_claim_territory import ResponseClaimTerritory
from engine.responses.response_place_initial_troop import ResponsePlaceInitialTroop
from engine.responses.response_redeem_card_decision import ResponseRedeemCardDecision
from engine.responses.response_place_player_troop import ResponsePlacePlayerTroop
from engine.responses.response_redeem_player_cards import ResponseRedeemPlayerCards

P = ParamSpec("P")
T = TypeVar("T")
def handle_sigpipe(fn: Callable[P, T]) -> Callable[P, T]:
    """Decorator to trigger ban if the player closes the from_engine pipe.
    """

    def dfn(*args: P.args, **kwargs: P.kwargs) -> T:
        self: 'PlayerConnection' = args[0] # type: ignore
        try:
            result = fn(*args, **kwargs)
        except BrokenPipeError:
            raise BrokenPipeException(self.player_id, "You closed 'from_engine.pipe'.")

        return result
    
    return dfn


def handle_invalid(fn: Callable[P, T]) -> Callable[P, T]:
    """Decorator to trigger ban if the player sends an invalid, but syntactically correct message.
    """

    def dfn(*args: P.args, **kwargs: P.kwargs) -> T:
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

    def dfn1(fn: Callable[P, T]):
        def dfn2(*args: P.args, **kwargs: P.kwargs) -> T:
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


@final
class PlayerConnection():

    def __init__(self, player_id: int):
        self.player_id = player_id
        self._to_engine_pipe: TextIOWrapper
        self._from_engine_pipe: TextIOWrapper
        self._cumulative_time: float = 0

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
    def query_claim_territory(self, state: State) -> ResponseClaimTerritory:
        data = QueryClaimTerritory(territories=state.territories.values(), players=state.players.values())
        self._send(data.model_dump_json())

        response = self._receive()
        return ResponseClaimTerritory.model_validate_json(response, context={"state": state, "player": self.player_id})

    @handle_invalid
    @handle_sigpipe
    @time_limited()
    def query_place_initial_troop(self, state: State) -> ResponsePlaceInitialTroop:
        data = QueryPlaceInitialTroop(territories=state.territories.values(), players=state.players.values())
        self._send(data.model_dump_json())
        
        response = self._receive()
        return ResponsePlaceInitialTroop.model_validate_json(response, context={"state": state, "player": self.player_id})
        
    @handle_invalid
    @handle_sigpipe
    @time_limited()
    def query_place_player_troop(self, state: State) -> ResponsePlacePlayerTroop:
        data = QueryPlacePlayerTroop(territories=state.territories.values(), players=state.players.values())
        self._send(data.model_dump_json())
        
        response = self._receive()
        return ResponsePlacePlayerTroop.model_validate_json(response, context={"state": state, "player": self.player_id})    
    
    @handle_invalid
    @handle_sigpipe
    @time_limited()
    def query_redeem_card_decision(self, state: State) -> ResponseRedeemCardDecision:
        data = QueryRedeemCardDecision(territories=state.territories.values(), players=state.players.values())
        self._send(data.model_dump_json())
        
        response = self._receive()
        return ResponseRedeemCardDecision.model_validate_json(response, context={"state": state, "player": self.player_id})
    
    @handle_invalid
    @handle_sigpipe
    @time_limited()
    def query_redeem_player_cards(self, state: State) -> ResponseRedeemPlayerCards:
        data = QueryRedeemPlayerCards(territories=state.territories.values(), players=state.players.values())
        self._send(data.model_dump_json())

        response = self._receive()
        return ResponseRedeemPlayerCards.model_validate_json(response, context={"state": state, "player": self.player_id})

if __name__ == "__main__":
    state = State()
    connection = PlayerConnection(player_id=0)

    try:
        connection.query_claim_territory(state)
    except EngineException as e:
        raise e