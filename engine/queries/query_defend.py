from typing import Literal

from engine.queries.base_query import BaseQuery


class QueryDefend(BaseQuery):
    query_type: Literal["defend"] = "defend"