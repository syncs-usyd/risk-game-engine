from typing import Literal

from risk_shared.queries.base_query import BaseQuery


class QueryTroopsAfterAttack(BaseQuery):
    query_type: Literal["troops_after_attack"] = "troops_after_attack"
    record_attack_id: int