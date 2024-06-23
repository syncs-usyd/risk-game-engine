from typing import Literal
from risk_shared.queries.base_query import BaseQuery


class QueryAttack(BaseQuery):
    query_type: Literal["attack"] = "attack"