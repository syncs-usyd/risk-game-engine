from engine.records.base_record import BaseRecord


class RecordStartTurn(BaseRecord):
    player: int
    continents_held: list[int]
    continent_bonus: int
    territory_bonus: int