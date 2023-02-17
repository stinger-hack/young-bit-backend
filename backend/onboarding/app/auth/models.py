from passlib.context import CryptContext
from sqlalchemy import Column, String, insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped

from onboarding.models import BaseModel

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Users(BaseModel):
    __tablename__ = "users"

    fullname: Mapped[str] = Column(String, nullable=True)  # e.g. Кобеев А.М.
    username: Mapped[str] = Column(String, unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = Column(String, nullable=False)

    @staticmethod
    async def get_by_username(username: str, session: AsyncSession):
        query = select(Users).where(Users.username == username)
        result = (await session.execute(query)).scalars().first()
        return result

    @staticmethod
    async def insert_data(username: str, hashed_password: str, session: AsyncSession):
        query = insert(Users).values(username=username, hashed_password=hashed_password)
        await session.execute(query)
        await session.commit()
