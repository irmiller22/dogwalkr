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


class DogsResponse(BaseModel):
    meta: Meta
    dogs: List[Dog]


class DogWithOwners(Dog):
    owner: User


class UsersResponse(BaseModel):
    meta: Meta
    users: List[User]


class UserWithDogs(User):
    dogs: List[Dog]
