from datetime import datetime

from pydantic import BaseModel


class Dog(BaseModel):
    id: int
    name: str
    owner_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
