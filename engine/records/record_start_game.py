from engine.records.base_record import BaseRecord


class RecordStartGame(BaseRecord):
    turn_order: list[int]