from pydantic import BaseModel
from pydantic_sqlalchemy import sqlalchemy_to_pydantic

from .db import UserDAO


User = sqlalchemy_to_pydantic(UserDAO)


class CreateUser(BaseModel):
    name: str
