import strawberry

from fastapi.encoders import jsonable_encoder
from typing import List
from datetime import datetime

from .db import get_db

from .models import User, Token
from .otypes import Info
from .otypes import SimpleUserType, FullUserType, UserSignUpInput, UserLoginInput, TokenType
from .utils import create_access_token, get_password_hash, verify_password
from .config import settings
from datetime import timedelta


db= get_db()

# user mutation
@strawberry.mutation
def signUp(userInput: UserSignUpInput) -> SimpleUserType:
    # Converting the input to pydantic model - json based
    user = jsonable_encoder(userInput.to_pydantic()) # type: ignore

    # hash pasword
    user["password"] = get_password_hash(password=user["password"])
    
    # add to database
    created_id = db.users.insert_one(user).inserted_id

    # query back from database
    created_user = User.model_validate(db.users.find_one({"_id": created_id}))

    # Returning back json, strawberry based model response
    return SimpleUserType.from_pydantic(created_user) # type: ignore


@strawberry.mutation
def login(userInput: UserLoginInput) -> TokenType:
    # Converting the input to pydantic model - json based
    user = jsonable_encoder(userInput.to_pydantic()) # type: ignore
    
    # get user from to database
    found_user = db.users.find_one({"email": user["email"]})

    if not found_user:
        raise Exception("User not found!")
    
    if not verify_password(user["password"], found_user["password"]):
        raise Exception("Incorrect email or password!")
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    
    jwt = Token.model_validate(
        {
            "access_token": create_access_token(
                user["email"], expires_delta=access_token_expires
            ),
            "token_type": "bearer",
        }
    )

    # Returning back json, strawberry based model response
    return TokenType.from_pydantic(jwt) # type: ignore


@strawberry.mutation
def userUpdate(userInput: UserSignUpInput, info: Info) -> FullUserType:
    user = info.context.user
    print(user)
    # Getting user context - for selective permissions

    input = jsonable_encoder(userInput.to_pydantic())  # type: ignore

    # update to database
    db.users.find_one_and_update({"_id": input["_id"]}, {"$set": {"name": "UPDATED", "date_time": str(datetime.utcnow)}})

    # query back from database
    created_user = User.model_validate(
        db.users.find_one({"_id": input["_id"]}))

    return FullUserType.from_pydantic(created_user)  # type: ignore

# register all mutations
mutations = [
    signUp,
    login,
    userUpdate
]