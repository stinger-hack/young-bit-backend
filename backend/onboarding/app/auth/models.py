from passlib.context import CryptContext
from sqlalchemy import Column, String, insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped

from onboarding.models import BaseModel

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Users(BaseModel):
    __tablename__ = "users"

    first_name: Mapped[str] = Column(String, nullable=False)
    last_name: Mapped[str] = Column(String, nullable=False)
    patronymic: Mapped[str] = Column(String, nullable=True)
    username: Mapped[str] = Column(String, unique=False, index=True, nullable=False)
    hashed_password: Mapped[str] = Column(String, nullable=False)
    role: Mapped[str] = Column(String(15), nullable=False)

    @staticmethod
    async def get_by_username(username: str, session: AsyncSession):
        query = select(Users).where(Users.username == username)
        result = (await session.execute(query)).scalars().first()
        return result

    @staticmethod
    async def insert_data(
        first_name: str,
        last_name: str,
        patronymic: str,
        username: str,
        hashed_password: str,
        role: str,
        session: AsyncSession,
    ):
        query = insert(Users).values(
            first_name=first_name,
            last_name=last_name,
            patronymic=patronymic,
            username=username,
            role=role,
            hashed_password=hashed_password,
        )
        await session.execute(query)
        await session.commit()
