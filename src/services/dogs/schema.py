from datetime import datetime
from typing import List

from pydantic import BaseModel

from ..common.schema import Meta


class Dog(BaseModel):
    id: int
    name: str
    owner_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class DogResponse(BaseModel):
    dog: Dog


class DogsResponse(BaseModel):
    meta: Meta
    dogs: List[Dog]


class CreateDog(BaseModel):
    name: str
    owner_id: int
