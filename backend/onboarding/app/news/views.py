from datetime import datetime
from onboarding.protocol import BaseModel
from onboarding.enums import NewsTypeEnum, UserRoleEnum


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
    user: UserPayload


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
    title: str
    main_text: str
    image_url: str
    user_id: int


class CreateNewsRequest(CreateInitiativeRequest):
    news_type: NewsTypeEnum
