from typing import Literal, Union

from engine.queries.base_query import BaseQuery


class QueryRedeemCards(BaseQuery):
    query_type: Literal["redeem_cards"] = "redeem_cards"
    cause: Union[Literal["turn_started"], Literal["player_eliminated"]]