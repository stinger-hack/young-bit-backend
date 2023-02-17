from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, select, and_, update
from sqlalchemy.orm import relationship, joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from onboarding.enums import NewsTypeEnum, ActionType

from onboarding.models import BaseDatetimeModel


class News(BaseDatetimeModel):
    __tablename__ = "news"

    title = Column(String(255), nullable=False)
    main_text = Column(String, nullable=True)
    image_url = Column(String(255), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("Users")
    news_type = Column(String(10), nullable=False)  # formal or informal news
    is_approved = Column(Boolean, nullable=True)  # None == not checked, False == not pass, True == pass

    @classmethod
    async def get_news(cls, news_type: NewsTypeEnum, session: AsyncSession):
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
