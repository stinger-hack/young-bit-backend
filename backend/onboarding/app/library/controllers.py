from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from onboarding.app.auth.models import Users
from onboarding.app.library.views import CreateBookRequest
from onboarding.auth.oauth2 import get_current_user
from onboarding.db import get_session
from onboarding.protocol import Response

from .models import UserBook, Book

router = APIRouter(dependencies=[Depends(get_current_user)])

@router.get("/library")
async def get_user_library(user: Users = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    result = await UserBook.get_book_by_user_id(user_id=user.id, session=session)
    group_category = {}
    for item in result:
        group_category[item.book.category] = group_category.get(item.book.category, [])
        group_category[item.book.category].append(item.book)
    return Response(body=group_category)


@router.post("/admin/library")
async def create_book(body: CreateBookRequest, session: AsyncSession = Depends(get_session)):
    await Book.insert_data(name=body.name, category=body.category, img_link=body.img_link, session=session)
    return Response()
