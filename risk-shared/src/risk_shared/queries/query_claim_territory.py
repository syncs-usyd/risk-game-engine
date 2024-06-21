from typing import Literal

from risk_shared.queries.base_query import BaseQuery


class QueryClaimTerritory(BaseQuery):
    query_type: Literal["claim_territory"] = "claim_territory"