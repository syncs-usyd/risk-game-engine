from typing import Literal, final

from risk_shared.records.base_record import BaseRecord

@final
class RecordTerritoryConquered(BaseRecord):
    record_type: Literal["record_territory_conquered"] = "record_territory_conquered"
    record_attack_id: int

