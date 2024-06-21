from typing import Literal

from risk_shared.queries.base_query import BaseQuery


class QueryDefend(BaseQuery):
    query_type: Literal["defend"] = "defend"
    move_attack_id: int