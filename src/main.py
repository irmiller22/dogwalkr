import graphene
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from graphene_pydantic import PydanticObjectType
from graphql.execution.executors.asyncio import AsyncioExecutor
from starlette.graphql import GraphQLApp


from src.services.dogs.schema import (
    CreateDog,
    Dog,
)
from src.services.users.schema import (
    CreateUser,
    User,
)
from src.services.common.schema import (
    Meta,
    DogResponse,
    DogsResponse,
    DogWithOwner,
    UserResponse,
    UsersResponse,
    UserWithDogs,
)
from src.services.dogs.db import DogsContextManager
from src.services.users.db import UsersContextManager


# GraphQL
class GQLUser(PydanticObjectType):
    class Meta:
        model = User

    dogs = graphene.List("src.main.GQLDog")

    def resolve_dogs(self, info):
        with DogsContextManager() as manager:
            results, _ = manager.get_dogs(owner_id=self.id)
            return [Dog.from_orm(result) for result in results]


class GQLCreateUser(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)

    ok = graphene.Boolean()
    user = graphene.Field(lambda: GQLUser)

    def mutate(root, info, name: str):
        with UsersContextManager() as manager:
            user = manager.create_user(name=name)
            return GQLCreateUser(user=User.from_orm(user), ok=True)


class GQLDog(PydanticObjectType):
    class Meta:
        model = Dog

    owner = graphene.Field("src.main.GQLUser")

    def resolve_owner(self, info):
        with UsersContextManager() as manager:
            owner = manager.get_user_by_id(user_id=self.owner_id)
            return User.from_orm(owner)


class GQLCreateDog(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        owner_id = graphene.Int(required=True)

    ok = graphene.Boolean()
    dog = graphene.Field(lambda: GQLDog)

    def mutate(root, info, name: str, owner_id: int):
        with DogsContextManager() as manager:
            dog = manager.create_dog(name=name, owner_id=owner_id)
            return GQLCreateDog(dog=Dog.from_orm(dog), ok=True)


class Query(graphene.ObjectType):
    dogs = graphene.List(
        GQLDog,
        name=graphene.String(required=False),
        owner_id=graphene.Int(required=False),
    )
    users = graphene.List(GQLUser)
    dog = graphene.Field(GQLDog, dog_id=graphene.Int())
    user = graphene.Field(GQLUser, user_id=graphene.Int())

    def resolve_dogs(self, info, name: str = None, owner_id: int = None):
        with DogsContextManager() as manager:
            results, _ = manager.get_dogs(name=name, owner_id=owner_id)
            return [Dog.from_orm(result) for result in results]

    def resolve_users(self, info):
        with UsersContextManager() as manager:
            results, _ = manager.get_users()
            return [User.from_orm(result) for result in results]

    def resolve_dog(self, info, dog_id: int):
        with DogsContextManager() as manager:
            result = manager.get_dog_by_id(dog_id=dog_id)
            return Dog.from_orm(result)

    def resolve_user(self, info, user_id: int):
        with UsersContextManager() as manager:
            result = manager.get_user_by_id(user_id=user_id)
            return User.from_orm(result)


class Mutations(graphene.ObjectType):
    create_dog = GQLCreateDog.Field()
    create_user = GQLCreateUser.Field()


app = FastAPI()
app.add_route(
    "/graphql",
    GraphQLApp(
        schema=graphene.Schema(query=Query, mutation=Mutations),
        executor_class=AsyncioExecutor,
    ),
)


@app.get("/")
async def main():
    return RedirectResponse(url="/redoc/")


@app.get("/dogs/", response_model=DogsResponse, tags=["Dogs"])
async def get_dogs(
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
            dogs=[DogWithOwner.from_orm(result) for result in results],
        )


@app.get("/dogs/{dog_id}", response_model=DogResponse, tags=["Dogs"])
async def get_dog(dog_id: int):
    with DogsContextManager() as manager:
        dog = manager.get_dog_by_id(dog_id)
        return DogResponse(dog=DogWithOwner.from_orm(dog))


@app.post("/dogs/", response_model=DogResponse, status_code=201, tags=["Dogs"])
async def post_dogs(dog: CreateDog):
    with DogsContextManager() as manager:
        try:
            dog = manager.create_dog(name=dog.name, owner_id=dog.owner_id)
        except Exception as e:
            raise HTTPException(status_code=404, detail=str(e))
        return DogResponse(dog=DogWithOwner.from_orm(dog))


@app.get("/users/", response_model=UsersResponse, tags=["Users"])
async def get_users():
    with UsersContextManager() as manager:
        results, count = manager.get_users(user_id=1)
        return UsersResponse(
            meta=Meta(total=count),
            users=[UserWithDogs.from_orm(result) for result in results],
        )


@app.get("/users/{user_id}", response_model=UserResponse, tags=["Users"])
async def get_user(user_id: int):
    with UsersContextManager() as manager:
        user = manager.get_user_by_id(user_id)
        return UserResponse(user=UserWithDogs.from_orm(user))


@app.post("/users/", response_model=UserResponse, status_code=201, tags=["Users"])
async def post_users(user: CreateUser):
    with UsersContextManager() as manager:
        user = manager.create_user(name=user.name)
        return UserResponse(user=User.from_orm(user))
