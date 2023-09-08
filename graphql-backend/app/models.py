from typing import (
    Any,
    Callable,
    Optional
)

from pydantic_core import core_schema
from typing_extensions import Annotated

from pydantic import (
    BaseModel,
    GetJsonSchemaHandler,
    BaseModel,
    Extra,
    Field,
    EmailStr,
    ConfigDict,
    SkipValidation
)
from pydantic.json_schema import JsonSchemaValue
from bson import ObjectId
from datetime import datetime
from enum import Enum
import strawberry

class _ObjectIdPydanticAnnotation:
    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source_type: Any,
        _handler: Callable[[Any], core_schema.CoreSchema],
    ) -> core_schema.CoreSchema:
        """
        We return a pydantic_core.CoreSchema that behaves in the following ways:

        * str will be parsed as `ObjectId` instances with the str as the id attribute
        * `ObjectId` instances will be parsed as `ObjectId` instances without any changes
        * Nothing else will pass validation
        * Serialization will always return just a str
        """

        def validate_from_str(__id: str) -> ObjectId:
            result = ObjectId(__id)
            return result

        from_str_schema = core_schema.chain_schema(
            [
                core_schema.str_schema(),
                core_schema.no_info_plain_validator_function(validate_from_str),
            ]
        )

        return core_schema.json_or_python_schema(
            json_schema=from_str_schema,
            python_schema=core_schema.union_schema(
                [
                    # check if it's an instance first before doing any further work
                    core_schema.is_instance_schema(ObjectId),
                    from_str_schema,
                ]
            ),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda instance: instance.__str__()
            ),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, _core_schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        # Use the same schema that would be used for `str`
        return handler(core_schema.str_schema())


# We now create an `Annotated` wrapper that we'll use as the annotation for fields on `BaseModel`s, etc.
PydanticObjectId = Annotated[
    str, _ObjectIdPydanticAnnotation
]

@strawberry.enum
class EnumTrial(str, Enum):
    online = 'online'
    offline = 'offline'

class User(BaseModel):
    id: PydanticObjectId = Field(default_factory=PydanticObjectId, alias="_id")
    name: Optional[str] = Field(..., min_length=0, max_length=100)
    email: str = Field(...)
    password: str = Field(...)
    status: EnumTrial = EnumTrial.offline
    date_time: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        str_strip_whitespace=True,
        str_max_length=200,
        validate_assignment=True,
        extra=Extra.forbid
    )


class UserInput(BaseModel):
    id: PydanticObjectId = Field(default_factory=PydanticObjectId, alias="_id")
    name: Optional[str] = Field(default=None)
    email: Optional[str] = Field(default=None)
    status: EnumTrial = EnumTrial.offline
    date_time: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        str_strip_whitespace=True,
        str_max_length=200,
        validate_assignment=True,
        extra=Extra.forbid
    )

class UserMuationInput(BaseModel):
    name: Optional[str] = Field(default=None)
    email: str = Field(...)
    password: str = Field(...)
    status: EnumTrial = EnumTrial.offline
    date_time: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        str_strip_whitespace=True,
        str_max_length=200,
        validate_assignment=True,
        extra=Extra.forbid
    )


class Token(BaseModel):
    access_token: str
    token_type: str
    