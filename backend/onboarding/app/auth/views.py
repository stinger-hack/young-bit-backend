from datetime import datetime

from pydantic import BaseModel as PydanticBaseModel

from onboarding.protocol import BaseModel


class Token(PydanticBaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str
    first_name: str
    last_name: str
    patronymic: str | None
    exp: datetime | None


class UserLogin(BaseModel):
    username: str
    password: str


class UserPayload(BaseModel):
    username: str
    first_name: str
    last_name: str
    patronymic: str | None
    img_link: str
    role: str
    score: int
    cards: list[str] = []


class LunchUserView(BaseModel):
    fullname: str
    img_link: str
    theme: str
