from pydantic import BaseModel
from pydantic_sqlalchemy import sqlalchemy_to_pydantic

from .db import DogDAO


Dog = sqlalchemy_to_pydantic(DogDAO)


class CreateDog(BaseModel):
    name: str
    owner_id: int
