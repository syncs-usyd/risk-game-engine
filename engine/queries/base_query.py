from pydantic import BaseModel


class BaseQuery(BaseModel):
    query_type: str