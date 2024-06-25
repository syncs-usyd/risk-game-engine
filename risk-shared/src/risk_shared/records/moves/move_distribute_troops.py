from typing import Literal, Union, final

from risk_shared.records.base_move import BaseMove

@final
class MoveDistributeTroops(BaseMove):
    record_type: Literal["move_distribute_troops"] = "move_distribute_troops"
    cause: Union[Literal["turn_started"], Literal["player_eliminated"]]
    distributions: dict[int, int] # territory_id, troop_count