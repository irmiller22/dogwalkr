from datetime import datetime
from typing import List

import graphene
from pydantic import BaseModel
from pydantic_sqlalchemy import sqlalchemy_to_pydantic

from .db import DogDAO


# REST
# class Dog(BaseModel):
#     id: int
#     name: str
#     owner_id: int
#     created_at: datetime
#     updated_at: datetime

#     class Config:
#         orm_mode = True

Dog = sqlalchemy_to_pydantic(DogDAO)


class DogResponse(BaseModel):
    dog: Dog


class CreateDog(BaseModel):
    name: str
    owner_id: int
