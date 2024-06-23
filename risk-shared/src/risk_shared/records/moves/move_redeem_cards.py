from typing import Literal, Tuple, Union, final

from risk_shared.records.base_move import BaseMove

@final
class MoveRedeemCards(BaseMove):
    record_type: Literal["move_redeem_cards"] = "move_redeem_cards"
    sets: list[Tuple[int, int, int]]
    cause: Union[Literal["turn_started"], Literal["player_eliminated"]]




        

