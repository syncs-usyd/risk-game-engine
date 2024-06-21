from typing import Literal

from engine.queries.base_query import BaseQuery


class QueryClaimTerritory(BaseQuery):
    query_type: Literal["claim_territory"] = "claim_territory"