from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from onboarding.protocol import Response

from .views import Token, TokenData
from onboarding.auth.hash import get_password_hash, verify_password  # isort:skip
from onboarding.auth.jwt_token import create_access_token  # isort:skip
from onboarding.db import get_session  # isort:skip
from onboarding.exceptions import UnauthorizedError  # isort:skip
from onboarding.app.auth.models import Users  # isort:skip
from onboarding.enums import UserRoleEnum

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
    token = create_access_token(
        TokenData(
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            patronymic=user.patronymic,
        )
    )
    return Token(access_token=token, token_type="Bearer")


@router.post("/register", response_model=Response)
async def register_user(
    username: str,
    password: str,
    role: UserRoleEnum,
    first_name: str,
    last_name: str,
    patronymic: str | None = None,
    session: AsyncSession = Depends(get_session),
):
    hashed_password = get_password_hash(password)
    await Users.insert_data(
        first_name=first_name,
        last_name=last_name,
        patronymic=patronymic,
        username=username,
        hashed_password=hashed_password,
        role=role,
        session=session,
    )
    return Response()
