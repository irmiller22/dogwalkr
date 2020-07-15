from typing import List, Optional

from fastapi import FastAPI
from fastapi.responses import RedirectResponse


from src.services.dogs.schema import Dog, DogsResponse
from src.services.users.schema import User, UsersResponse
from src.services.common.db import engine
from src.services.common.models import Base
from src.services.common.schema import Meta
from src.services.dogs.db import DogsContextManager, DogDAO
from src.services.users.db import UsersContextManager, UserDAO


app = FastAPI()


@app.get("/")
def main():
    return RedirectResponse(url="/docs/")


@app.get("/dogs/", response_model=DogsResponse, tags=["Dogs"])
def get_dogs():
    with DogsContextManager() as manager:
        results, count = manager.get_dogs(name="test")
        return DogsResponse(
            meta=Meta(total=count), dogs=[Dog.from_orm(result) for result in results]
        )


@app.get("/users/", response_model=UsersResponse, tags=["Users"])
def get_users():
    with UsersContextManager() as manager:
        results, count = manager.get_users(user_id=1)
        return UsersResponse(
            meta=Meta(total=count), users=[User.from_orm(result) for result in results]
        )
