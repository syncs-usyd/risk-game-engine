from typing import Literal, Union

from risk_shared.queries.base_query import BaseQuery


class QueryDistributeTroops(BaseQuery):
    query_type: Literal["distribute_troops"] = "distribute_troops"
    cause: Union[Literal["turn_started"], Literal["player_eliminated"]]