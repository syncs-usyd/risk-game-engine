import math

from pydantic import Field, RootModel, TypeAdapter
from risk_shared.queries.query_type import QueryType
from risk_shared.records.types.move_type import MoveType

MAX_CHARACTERS_READ = 1000000
READ_CHUNK_SIZE = 1024

class DiscriminatedTypeAdapter(RootModel):
    root: QueryType = Field(discriminator="query_type")

class Connection():

    def __init__(self):
        self._to_engine_pipe = open(f"./io/to_engine.pipe", "w")
        self._from_engine_pipe = open(f"./io/from_engine.pipe", "r")

    
    def _send(self, data: str) -> None:
        self._to_engine_pipe.write(str(len(data)) + ",")
        self._to_engine_pipe.write(data)
        self._to_engine_pipe.flush()

    
    def _receive(self) -> str:
        
        # Read size of message.
        buffer = bytearray()
        while len(buffer) < math.floor(math.log10(MAX_CHARACTERS_READ)) + 1 and (len(buffer) == 0 or buffer[-1] != ord(",")):
            buffer.extend(self._from_engine_pipe.read(1).encode())

        if buffer[-1] == ord(","):
            size = int(buffer[0:-1].decode())
        else:
            print(buffer)
            raise RuntimeError("Please send us a discord message with this error log.")
        
        if size > MAX_CHARACTERS_READ:
            raise RuntimeError("Please send us a discord message with this error log.")
        
        # Read message.
        buffer = bytearray()
        while len(buffer) < size:
            buffer.extend(bytearray(self._from_engine_pipe.read(min((size - len(buffer)), READ_CHUNK_SIZE)).encode()))

        return buffer.decode()
    

    def get_next_query(self) -> QueryType:
        return DiscriminatedTypeAdapter.model_validate_json(self._receive()).root


    def send_move(self, move: MoveType):
        self._send(move.model_dump_json())