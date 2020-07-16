from typing import List, Optional

from pydantic import BaseModel

from ..dogs.schema import Dog
from ..users.schema import User


class Meta(BaseModel):
    total: int
    limit: Optional[int]
    offset: Optional[int]
    sort: Optional[str]
    order: Optional[str]


class DogWithOwner(Dog):
    owner: User


class DogResponse(BaseModel):
    dog: DogWithOwner


class DogsResponse(BaseModel):
    meta: Meta
    dogs: List[DogWithOwner]


class UserWithDogs(User):
    dogs: List[Dog]


class UserResponse(BaseModel):
    user: UserWithDogs


class UsersResponse(BaseModel):
    meta: Meta
    users: List[UserWithDogs]
