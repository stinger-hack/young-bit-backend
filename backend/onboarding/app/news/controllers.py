import uuid
from fastapi import APIRouter, Depends, WebSocket, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from .models import Action, News
from .views import ApprovedNewsRequest, LikesView, NewsView, CommentsView
from onboarding.auth.oauth2 import get_current_user
from onboarding.config import settings
from onboarding.db import get_session
from onboarding.enums import ActionType, NewsTypeEnum
from onboarding.storage.s3 import S3Service
from onboarding.protocol import Response

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.websocket("/sos/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await websocket.accept()
    while True:
        data = await websocket.receive_json()
        await websocket.receive_json({"data": f"received {data}"})


@router.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):
    client: S3Service = await S3Service.get_s3_client()
    contents = await file.read()
    filename = f"{uuid.uuid4().hex}.{file.filename.rsplit('.')[-1].lower()}"
    await client.put_object(Bucket=settings.BUCKET_NAME, Key=filename, Body=contents)
    img_link = S3Service.get_img_link(filename)
    return Response(body={"img_link": img_link})


@router.get("/news", response_model=Response[list[NewsView]])
async def get_news(news_type: NewsTypeEnum, session: AsyncSession = Depends(get_session)):
    result = await News.get_news(news_type=news_type, session=session)
    return Response(body=[NewsView.from_orm(item) for item in result])


@router.get("/comments/{news_id}")
async def get_comments(news_id: int, session: AsyncSession = Depends(get_session)):
    result = await Action.get_actions(ActionType.COMMENT, news_id=news_id, session=session)
    return Response(body=[CommentsView.from_orm(item) for item in result])


@router.get("/likes/{news_id}")
async def get_likes(news_id: int, session: AsyncSession = Depends(get_session)):
    result = await Action.get_actions(ActionType.LIKE, news_id=news_id, session=session)
    return Response(body=[LikesView.from_orm(item) for item in result])


@router.post("admin/news/approve_news")
async def approve_post(body: ApprovedNewsRequest, session: AsyncSession = Depends(get_session)):
    await News.approve_news(news_id=body.news_id, is_approved=body.is_approved, session=session)
    return Response
