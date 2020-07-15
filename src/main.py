import graphene
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from starlette.graphql import GraphQLApp


from src.services.dogs.schema import (
    CreateDog,
    Dog,
    DogResponse,
    DogsResponse,
)
from src.services.users.schema import (
    CreateUser,
    User,
    UserResponse,
    UsersResponse,
)
from src.services.common.db import engine
from src.services.common.models import Base
from src.services.common.schema import Meta
from src.services.dogs.db import DogsContextManager
from src.services.users.db import UsersContextManager


class Query(graphene.ObjectType):
    hello = graphene.String(name=graphene.String(default_value="stranger"))

    def resolve_hello(self, info, name):
        return "Hello " + name


app = FastAPI()
app.add_route("/graphql", GraphQLApp(schema=graphene.Schema(query=Query)))


@app.get("/")
def main():
    return RedirectResponse(url="/redoc/")


@app.get("/dogs/", response_model=DogsResponse, tags=["Dogs"])
def get_dogs(
    name: str = None,
    owner_id: int = None,
    sort: str = "created_at",
    order: str = "desc",
    limit: int = 100,
    offset: int = 0,
):
    with DogsContextManager() as manager:
        results, count = manager.get_dogs(
            name=name,
            owner_id=owner_id,
            sort=sort,
            order=order,
            limit=limit,
            offset=offset,
        )
        return DogsResponse(
            meta=Meta(total=count, sort=sort, order=order, limit=limit, offset=offset,),
            dogs=[Dog.from_orm(result) for result in results],
        )


@app.get("/dogs/{dog_id}", response_model=DogResponse, tags=["Dogs"])
def get_dog(dog_id: int):
    with DogsContextManager() as manager:
        dog = manager.get_dog_by_id(dog_id)
        return DogResponse(dog=Dog.from_orm(dog))


@app.post("/dogs/", response_model=DogResponse, status_code=201, tags=["Dogs"])
def post_dogs(dog: CreateDog):
    with DogsContextManager() as manager:
        try:
            dog = manager.create_dog(name=dog.name, owner_id=dog.owner_id)
        except Exception as e:
            raise HTTPException(status_code=404, detail=str(e))
        return DogResponse(dog=Dog.from_orm(dog))


@app.get("/users/", response_model=UsersResponse, tags=["Users"])
def get_users():
    with UsersContextManager() as manager:
        results, count = manager.get_users(user_id=1)
        return UsersResponse(
            meta=Meta(total=count), users=[User.from_orm(result) for result in results]
        )


@app.get("/users/{user_id}", response_model=UserResponse, tags=["Users"])
def get_user(user_id: int):
    with UsersContextManager() as manager:
        user = manager.get_user_by_id(user_id)
        return UserResponse(user=User.from_orm(user))


@app.post("/users/", response_model=UserResponse, status_code=201, tags=["Users"])
def post_users(user: CreateUser):
    with UsersContextManager() as manager:
        user = manager.create_user(name=user.name)
        return UserResponse(user=User.from_orm(user))
