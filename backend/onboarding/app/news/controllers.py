import asyncio
import uuid
from fastapi import APIRouter, Depends, WebSocket, UploadFile, File, WebSocketDisconnect
from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncSession
from .models import Action, Important, ImportantUser, News
from .views import (
    ApprovedNewsRequest,
    CreateImportantNews,
    CreateInitiativeRequest,
    ImportantNewsView,
    LikesView,
    NewsView,
    CommentsView,
    CreateNewsRequest,
)
from onboarding.auth.oauth2 import get_current_user
from onboarding.config import settings
from onboarding.db import get_session
from onboarding.enums import ActionType, NewsTypeEnum
from onboarding.storage.s3 import S3Service
from onboarding.protocol import Response

from onboarding.db import sync_maker
from operator import attrgetter

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.websocket("/sos/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await websocket.accept()
    while True:
        data = await websocket.receive_json()
        await websocket.send_json({"data": f"received {data}"})


@router.websocket("/important/{user_id}")
async def dashboard_data(websocket: WebSocket, user_id: int, session: AsyncSession = Depends(get_session)):
    flag = asyncio.Event()
    last_id = None

    @event.listens_for(sync_maker, "before_commit")
    def before_commit(session):
        last_commited_id = asyncio.run(ImportantUser.get_last_id())
        if last_commited_id > last_id:
            flag.set()

    await websocket.accept()
    result = await ImportantUser.get_by_user_id(user_id=user_id, session=session)  # get all important messages
    result_list = [
        ImportantNewsView(
            id=item.important.id,
            title=item.important.title,
            main_text=item.important.main_text,
            created_at=item.important.created_at.isoformat(),
        ).dict()
        for item in result
    ]
    last_id = max(result_list, key=lambda x: x["id"])
    await websocket.send_json({"data": result_list})
    while True:
        try:
            await flag.wait()
            await websocket.send_json(result_list)
            flag.clear()
        except WebSocketDisconnect:
            return None


@router.post("/admin/important")
async def create_important_news(body: CreateImportantNews, session: AsyncSession = Depends(get_session)):
    await ImportantUser.insert_data(user_id=body.user_id, important_id=body.important_id, session=session)
    await session.commit()
    return Response()


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
    result = await News.get_user_news(news_type=news_type, session=session)
    return Response(body=[NewsView.from_orm(item) for item in result])


@router.post("/initiative", response_model=Response[list[NewsView]])
async def create_initiative(body: CreateInitiativeRequest, session: AsyncSession = Depends(get_session)):
    await News.create_initiative(
        title=body.title,
        main_text=body.main_text,
        image_url=body.image_url,
        user_id=body.user_id,
        session=session,
    )
    return Response()


@router.get("/comments/{news_id}")
async def get_comments(news_id: int, session: AsyncSession = Depends(get_session)):
    result = await Action.get_actions(ActionType.COMMENT, news_id=news_id, session=session)
    return Response(body=[CommentsView.from_orm(item) for item in result])


@router.get("/likes/{news_id}")
async def get_likes(news_id: int, session: AsyncSession = Depends(get_session)):
    result = await Action.get_actions(ActionType.LIKE, news_id=news_id, session=session)
    return Response(body=[LikesView.from_orm(item) for item in result])


@router.get("/admin/news", response_model=Response[list[NewsView]])
async def get_news(news_type: NewsTypeEnum, session: AsyncSession = Depends(get_session)):
    result = await News.get_admin_news(news_type=news_type, session=session)
    return Response(body=[NewsView.from_orm(item) for item in result])


@router.post("/admin/news", response_model=Response[list[NewsView]])
async def get_news(body: CreateNewsRequest, session: AsyncSession = Depends(get_session)):
    await News.insert_data(
        title=body.title,
        main_text=body.main_text,
        image_url=body.image_url,
        user_id=body.user_id,
        news_type=body.news_type,
        session=session,
    )
    return Response()


@router.post("/admin/news/approve_news")
async def approve_post(body: ApprovedNewsRequest, session: AsyncSession = Depends(get_session)):
    await News.approve_news(news_id=body.news_id, is_approved=body.is_approved, session=session)
    return Response()
