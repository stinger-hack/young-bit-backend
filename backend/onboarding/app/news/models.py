from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, select, and_, update, insert
from sqlalchemy.orm import relationship, joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from onboarding.enums import NewsTypeEnum, ActionType

from onboarding.models import BaseModel, BaseDatetimeModel


class News(BaseDatetimeModel):
    __tablename__ = "news"

    title = Column(String(255), nullable=False)
    main_text = Column(String, nullable=True)
    image_url = Column(String(255), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    user = relationship("Users")
    news_type = Column(String(10), nullable=False)  # formal or informal news
    is_approved = Column(Boolean, nullable=True)  # None == not checked, False == not pass, True == pass

    @classmethod
    async def insert_data(
        cls, title: str, main_text: str, image_url: str, user_id: int, news_type: NewsTypeEnum, session: AsyncSession
    ):
        stmt = insert(cls).values(
            title=title, main_text=main_text, image_url=image_url, user_id=user_id, news_type=news_type
        )
        await session.execute(stmt)
        await session.commit()

    @classmethod
    async def create_initiative(
        cls, title: str, main_text: str, image_url: str | None, user_id: int, session: AsyncSession
    ):
        await cls.insert_data(
            title=title,
            main_text=main_text,
            image_url=image_url,
            user_id=user_id,
            news_type=NewsTypeEnum.INITIATIVE,
            session=session,
        )

    @classmethod
    async def get_admin_news(cls, news_type: NewsTypeEnum, session: AsyncSession):
        stmt = (
            select(cls)
            .where(
                and_(
                    cls.news_type == news_type,
                    cls.is_approved == None,
                )
            )
            .order_by(cls.created_at.desc())
            .options(joinedload(cls.user))
        )
        result = (await session.execute(stmt)).scalars()
        return result

    @classmethod
    async def get_user_news(cls, news_type: NewsTypeEnum, session: AsyncSession):
        stmt = (
            select(cls)
            .where(
                and_(
                    cls.news_type == news_type,
                    cls.is_approved == True,
                )
            )
            .order_by(cls.created_at.desc())
            .options(joinedload(cls.user))
        )
        result = (await session.execute(stmt)).scalars()
        return result

    @classmethod
    async def approve_news(cls, news_id, is_approved: bool, session: AsyncSession):
        stmt = update(cls).where(cls.id == news_id).values(is_approved=is_approved)
        await session.execute(stmt)
        await session.commit()


class Action(BaseDatetimeModel):
    __tablename__ = "actions"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("Users")
    action_type = Column(String(10), nullable=False)  # like or comment
    content = Column(String, nullable=True)  # text for comment
    news_id = Column(Integer, ForeignKey("news.id"))

    @classmethod
    async def get_actions(cls, action_type: ActionType, news_id: int, session: AsyncSession):
        stmt = (
            select(cls)
            .where(
                and_(
                    cls.news_id == news_id,
                    cls.action_type == action_type,
                )
            )
            .order_by(cls.created_at.desc())
            .options(joinedload(cls.user))
        )
        result = (await session.execute(stmt)).scalars()
        return result


class Important(BaseDatetimeModel):
    __tablename__ = "important_news"

    title = Column(String(255), nullable=False)
    main_text = Column(String, nullable=True)
    creator_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    @classmethod
    async def insert_data(cls, title: str, main_text: str, creator_id: str):
        ...


class ImportantUser(BaseModel):
    __tablename__ = "important_users"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    important_id = Column(Integer, ForeignKey("important_news.id"), nullable=False)
    important = relationship("Important")

    @classmethod
    async def get_last_id(cls, session: AsyncSession):
        stmt = select(max(cls.id))
        result = await session.execute(stmt).scalars()
        return result

    @classmethod
    async def insert_data(cls, user_id: int, important_id: int, session: AsyncSession):
        stmt = insert(cls).values(user_id=user_id, important_id=important_id)
        await session.execute(stmt)

    @classmethod
    async def get_by_user_id(cls, user_id: int, session: AsyncSession, last_id: int | None = None):
        stmt = (
            select(cls)
            .where(cls.user_id == user_id)
            .order_by(cls.important_id.desc())
            .options(joinedload(cls.important))
        )
        if last_id:
            stmt = stmt.where(cls.important_id > last_id)
        result = (await session.execute(stmt)).scalars()
        return result
