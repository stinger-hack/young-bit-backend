# import asyncio
# import uuid
# from fastapi import APIRouter, Depends, WebSocket, UploadFile, File, WebSocketDisconnect
# from sqlalchemy import event
# from sqlalchemy.ext.asyncio import AsyncSession
# from .models import Action, ImportantUser, News
# from .views import ApprovedNewsRequest, LikesView, NewsView, CommentsView
# from onboarding.auth.oauth2 import get_current_user
# from onboarding.config import settings
# from onboarding.db import get_session
# from onboarding.enums import ActionType, NewsTypeEnum
# from onboarding.storage.s3 import S3Service
# from onboarding.protocol import Response

# router = APIRouter(dependencies=[Depends(get_current_user)])


# @router.post("/admin/news/approve_news")
# async def approve_post(body: ApprovedNewsRequest, session: AsyncSession = Depends(get_session)):
#     await News.approve_news(news_id=body.news_id, is_approved=body.is_approved, session=session)
#     return Response()
