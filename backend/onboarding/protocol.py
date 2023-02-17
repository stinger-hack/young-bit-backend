from datetime import datetime
from typing import TypeVar
from uuid import UUID

import orjson
from pydantic import BaseModel as PydanticModel
from pydantic import Field, constr
from pydantic.generics import GenericModel as PydanticGenericModel
from pydantic.schema import Generic
from starlette.status import HTTP_200_OK


DataT = TypeVar("DataT")

iin_type = constr(regex=r"^\d{12}$")
age_field = Field(None, ge=0, description="Возраст")


def orjson_dumps(v, *, default):
    # orjson.dumps returns bytes, to match standard json.dumps we need to decode
    return orjson.dumps(v, default=default).decode()


def to_camel_case(snake_str: str) -> str:
    components = snake_str.split("_")
    return components[0] + "".join(x.title() for x in components[1:])


class BaseModel(PydanticModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
        orm_mode = True
        allow_population_by_field_name = True


class Response(PydanticGenericModel, Generic[DataT]):
    """
    Базовый ответ на запрос
    """

    code: int = Field(HTTP_200_OK, description="Код ответа (http-like)")
    message: str | None = Field(description="Описание кода ответа")
    body: DataT | None = Field(description="Тело ответа")

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
