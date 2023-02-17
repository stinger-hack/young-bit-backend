from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from onboarding.app.auth.models import Users
from onboarding.app.auth.views import TokenData
from onboarding.auth.jwt_token import decode_token
from onboarding.db import get_session
from onboarding.exceptions import UnauthorizedError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth")


async def get_current_user(
    token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)
) -> TokenData:
    token = decode_token(token)
    user = await Users.get_by_username(token.username, session)
    if not user:
        raise UnauthorizedError
    return user
