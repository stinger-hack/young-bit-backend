from fastapi import APIRouter, Depends
from onboarding.app.auth.models import Users
from onboarding.auth.oauth2 import get_current_user, decode_token

from onboarding.protocol import Response

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.post("/profile", response_model=Response)
def get_user_profile(user: Users = Depends(get_current_user)):
    return Response(body=user)
