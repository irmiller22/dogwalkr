from datetime import datetime
from typing import List

from pydantic import BaseModel

from ..common.schema import Meta


class User(BaseModel):
    id: int
    name: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class CreateUser(BaseModel):
    name: str


class UserResponse(BaseModel):
    user: User


class UsersResponse(BaseModel):
    meta: Meta
    users: List[User]
