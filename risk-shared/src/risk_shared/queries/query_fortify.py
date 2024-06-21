from typing import Literal

from risk_shared.queries.base_query import BaseQuery


class QueryFortifyTerritory(BaseQuery):
    query_type: Literal["fortify"] = "fortify"