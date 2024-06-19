from typing import Literal

from engine.queries.base_query import BaseQuery


class QueryDistributeTroops(BaseQuery):
    query_type: Literal["distribute_troops"] = "distribute_troops"