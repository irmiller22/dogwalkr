from datetime import datetime

from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str
    created_at: datetime
    updated_at: datetime
