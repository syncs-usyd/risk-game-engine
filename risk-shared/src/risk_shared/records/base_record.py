from pydantic import BaseModel

class BaseRecord(BaseModel):
    record_type: str