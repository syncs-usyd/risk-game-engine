from typing import Literal

from engine.queries.base_query import BaseQuery

class QueryAttack(BaseQuery):
    query_type: Literal["attack"] = "attack"