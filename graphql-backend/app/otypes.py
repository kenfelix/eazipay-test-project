import json
import strawberry

from strawberry.fastapi import BaseContext
from strawberry.types import Info as _Info
from strawberry.types.info import RootValueType

from typing import Union, Dict, Optional
from functools import cached_property

from .models import PydanticObjectId, User, Token, UserInput, UserMuationInput

# custom context class
class Context(BaseContext):
    @cached_property
    def user(self) -> Union[Dict, None]:
        if not self.request:
            return None

        user = json.loads(self.request.headers.get("user", "{}"))
        return user


# custom info type
Info = _Info[Context, RootValueType]

# serialize PydanticObjectId as a scalar type
PydanticObjectIdType = strawberry.scalar(
    PydanticObjectId, serialize=str, parse_value=lambda v: PydanticObjectId(v)
)


@strawberry.experimental.pydantic.type(model=Token, all_fields=True)
class TokenType:
    pass

# user object type from pydantic model with all fields exposed
@strawberry.experimental.pydantic.type(model=User, all_fields=True)
class FullUserType:
    pass


@strawberry.experimental.pydantic.type(model=User, fields=[
    "name",
    "email",
    "status"
])
class SimpleUserType:
    pass

# user query's input type from pydantic model
@strawberry.experimental.pydantic.input(model=UserInput, fields=[
    "name",
    "email",
    "status",
    "date_time"
])
class UserQueryInput:
    email: strawberry.auto


# user mutation's input type from pydantic model
@strawberry.experimental.pydantic.input(model=UserMuationInput, fields=[
    "name",
    "email",
    "password"
])
class UserSignUpInput:
    pass


@strawberry.experimental.pydantic.input(model=UserMuationInput, fields=[
    "email",
    "password"
])
class UserLoginInput:
    pass