from typing import Literal

from engine.queries.base_query import BaseQuery


class QueryRedeemCards(BaseQuery):
    query_type: Literal["redeem_cards"] = "redeem_cards"