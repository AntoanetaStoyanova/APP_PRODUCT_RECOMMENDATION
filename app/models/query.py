from pydantic import BaseModel

class Query(BaseModel):
    flavor: str
