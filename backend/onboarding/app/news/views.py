from datetime import datetime
from onboarding.protocol import BaseModel
from onboarding.enums import NewsTypeEnum, UserRoleEnum
from pydantic import validator


class UserPayload(BaseModel):
    first_name: str
    last_name: str
    patronymic: str | None
    username: str
    role: UserRoleEnum
    img_link: str


class NewsView(BaseModel):
    id: int
    title: str
    news_type: NewsTypeEnum
    created_at: datetime | str
    updated_at: datetime | str | None
    main_text: str
    image_url: str | None
    user: UserPayload | None = UserPayload(
        first_name="anonymous",
        last_name="user",
        username="anonymous",
        role=UserRoleEnum.EMPLOYEE,
        img_link="https://storage.yandexcloud.net/onboarding/ffd38812bdf14692b59bb89d1023ffa4.png",
    )


class CommentsView(BaseModel):
    id: int
    content: str
    created_at: datetime | str
    updated_at: datetime | str | None
    user: UserPayload


class LikesView(BaseModel):
    id: int
    created_at: datetime | str
    updated_at: datetime | str | None
    user: UserPayload


class ApprovedNewsRequest(BaseModel):
    news_id: int
    is_approved: bool


class CreateInitiativeRequest(BaseModel):
    title: str = "title"
    main_text: str
    img_link: str | None
    tags: str = '#НовостьДня'
    is_anonymous: bool = False


class CreateNewsRequest(CreateInitiativeRequest):
    news_type: NewsTypeEnum


class CreateImportantNews(BaseModel):
    user_id: int
    important_id: int


class ImportantNewsView(BaseModel):
    id: int
    title: str
    main_text: str
    created_at: str
