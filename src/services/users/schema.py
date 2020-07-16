from datetime import datetime
from typing import List

import graphene
from pydantic import BaseModel
from pydantic_sqlalchemy import sqlalchemy_to_pydantic

from .db import UserDAO


# REST
# class User(BaseModel):
#     id: int
#     name: str
#     created_at: datetime
#     updated_at: datetime

#     class Config:
#         orm_mode = True
User = sqlalchemy_to_pydantic(UserDAO)


class CreateUser(BaseModel):
    name: str


class UserResponse(BaseModel):
    user: User
