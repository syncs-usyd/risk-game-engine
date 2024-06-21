from typing import Literal

from risk_shared.queries.base_query import BaseQuery


class QueryPlaceInitialTroop(BaseQuery):
    query_type: Literal["place_initial_troop"] = "place_initial_troop"