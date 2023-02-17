from datetime import datetime
from onboarding.protocol import BaseModel
from onboarding.enums import NewsTypeEnum, UserRoleEnum


class UserPayload(BaseModel):
    first_name: str
    last_name: str
    patronymic: str | None
    username: str
    role: UserRoleEnum


class NewsView(BaseModel):
    title: str
    news_type: NewsTypeEnum
    created_at: datetime | str
    updated_at: datetime | str | None
    deleted_at: datetime | str | None
    id: int
    main_text: str
    image_url: str
    user: UserPayload
