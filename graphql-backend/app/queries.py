import strawberry

from fastapi.encoders import jsonable_encoder
from typing import List

from .db import get_db

# import all models and types
from .models import User
from .otypes import Info
from .otypes import SimpleUserType, FullUserType, UserQueryInput

db = get_db()

# user query
@strawberry.field
def user(userInput: UserQueryInput, info: Info) -> FullUserType:
    user = info.context.user
    print("user:", user)
    # Getting user context - for selective permissions

    user = jsonable_encoder(userInput.to_pydantic())  # type: ignore
    # Converting the input to pydantic model - json based

    # query from database
    found_user = db.users.find_one({"email": user["email"]})

    # handle missing user
    if found_user:
        found_user = User.model_validate(found_user)
        return FullUserType.from_pydantic(found_user)  # type: ignore
    else:
        raise Exception("User not found!")


# Query Returning List of values
@strawberry.field
def users(info: Info) -> List[SimpleUserType]:
    user = info.context.user
    print("user:", user)
    # Getting user context - for selective permissions

    results = db.users.find()

    if results:
        users = []
        for result in results:
            users.append(SimpleUserType.from_pydantic(User.model_validate(result)))  # type: ignore
        return users
    else:
        raise Exception("No User Result Found")


# register all queries
queries = [
    user,
    users
]