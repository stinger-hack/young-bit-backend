from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from .views import Token, TokenData
from onboarding.auth.hash import verify_password  # isort:skip
from onboarding.auth.jwt_token import create_access_token  # isort:skip
from onboarding.db import get_session  # isort:skip
from onboarding.exceptions import UnauthorizedError  # isort:skip
from onboarding.app.auth.models import Users  # isort:skip


router = APIRouter()


@router.post("/auth", response_model=Token)
async def authenticate_user(
    form_data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_session)
):
    user = await Users.get_by_username(form_data.username, session)
    if not user:
        raise UnauthorizedError
    if not verify_password(form_data.password, user.hashed_password):
        raise UnauthorizedError
    token = create_access_token(TokenData(username=user.username))
    return Token(access_token=token, token_type="Bearer")
