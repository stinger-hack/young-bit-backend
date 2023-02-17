from datetime import datetime, timedelta
from typing import Optional

import jwt
import pytz
from jwt.exceptions import PyJWTError
from pydantic import ValidationError

from onboarding.app.auth.views import TokenData
from onboarding.config import settings
from onboarding.exceptions import UnauthorizedError


def create_access_token(data: TokenData, expires_delta: Optional[timedelta] = None) -> str:
    if expires_delta:
        expire = datetime.now(pytz.UTC) + expires_delta
    else:
        expire = datetime.now(pytz.UTC) + timedelta(seconds=settings.AUTH_EXPIRES_SECONDS)
    data.exp = expire
    encoded_jwt = jwt.encode(dict(data), settings.AUTH_PRIVATE_KEY_DATA, algorithm=settings.AUTH_ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> TokenData:
    try:
        payload = jwt.decode(token, settings.AUTH_PUBLIC_KEY_DATA, algorithms=[settings.AUTH_ALGORITHM])
        if not payload:
            raise UnauthorizedError
        token_data = TokenData(**payload)
        if datetime.now(pytz.UTC) > token_data.exp:
            raise UnauthorizedError
    except PyJWTError as e:
        raise UnauthorizedError from e
    except ValidationError as e:
        raise UnauthorizedError from e
    return token_data
