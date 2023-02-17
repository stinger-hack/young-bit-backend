from datetime import datetime

from pydantic import BaseModel as PydanticBaseModel

from onboarding.protocol import BaseModel


class Token(PydanticBaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str
    exp: datetime | None


class UserLogin(BaseModel):
    username: str
    password: str
