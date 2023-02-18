from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, select, and_, update, insert
from sqlalchemy.orm import relationship, joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from onboarding.enums import NewsTypeEnum, ActionType

from onboarding.models import BaseModel, BaseDatetimeModel


class Book(BaseDatetimeModel):
    __tablename__ = "books"

    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    img_link = Column(String, nullable=False)
    progress = Column(Integer, nullable=False, default=0)

    @classmethod
    async def insert_data(cls, name: str, category: str, img_link: str, session: AsyncSession):
        stmt = insert(cls).values(name=name, category=category, img_link=img_link)
        await session.execute(stmt)
        await session.commit()


class UserBook(BaseModel):
    __tablename__ = "user_books"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    book = relationship("Book")

    @classmethod
    async def get_book_by_user_id(cls, user_id: int, session: AsyncSession):
        stmt = select(cls).where(cls.user_id == user_id).options(joinedload(cls.book))
        result = (await session.execute(stmt)).scalars()
        return result
