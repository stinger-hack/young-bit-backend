from fastapi import APIRouter
from onboarding.db import init_db

from onboarding.protocol import Response

router = APIRouter()


@router.get(
    "/healthz",
    response_model=Response,
)
async def get_healthcheck():
    return Response()


@router.post(
    "/init_db",
    response_model=Response,
)
async def post_init_db():
    await init_db()
    return Response()
