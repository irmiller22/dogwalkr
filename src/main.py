from typing import List, Optional

from fastapi import FastAPI
from fastapi.responses import RedirectResponse


from src.services.dogs.models import Dog
from src.services.users.models import User
from src.services.common.db import engine
from src.services.common.models import Base
from src.services.dogs.db import DogsContextManager, DogDAO
from src.services.users.db import UsersContextManager, UserDAO

Base.metadata.create_all(bind=engine)


app = FastAPI()


@app.get("/")
def main():
    return RedirectResponse(url="/docs/")


@app.get("/dogs/", response_model=List[Dog])
def get_dogs():
    with DogsContextManager() as manager:
        return manager.get_dogs(name="test")


@app.get("/users/", response_model=List[User])
def get_users():
    with UsersContextManager() as manager:
        return manager.get_users(user_id=1)
