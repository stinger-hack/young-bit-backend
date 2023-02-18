from passlib.context import CryptContext
from sqlalchemy import Column, String, insert, select, Integer, ForeignKey
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
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    role: Mapped[str] = Column(String(15), nullable=False)
    img_link: Mapped[str] = Column(
        String, nullable=True, default="https://storage.yandexcloud.net/onboarding/ffd38812bdf14692b59bb89d1023ffa4.png"
    )

    card_map = {
        0: [1, 2, 5, 6],
        1: [3, 5, 8],
        2: [
            8,
        ],
        3: [1, 6],
        4: [1, 2, 3, 4, 5, 6],
        5: [4, 7],
    }

    @classmethod
    async def get_all(cls, session: AsyncSession):
        stmt = select(cls)
        result = (await session.execute(stmt)).scalars()
        return result

    @classmethod
    async def get_by_department_id(cls, department_id: int, session: AsyncSession):
        stmt = select(cls).where(department_id == department_id)
        result = (await session.execute(stmt)).scalars()
        return result

    @staticmethod
    async def get_by_username(username: str, session: AsyncSession):
        stmt = select(Users).where(Users.username == username)
        result = (await session.execute(stmt)).scalars().first()
        return result

    @staticmethod
    async def get_by_id(user_id: int, session: AsyncSession):
        stmt = select(Users).where(Users.id == user_id)
        result = (await session.execute(stmt)).scalars().first()
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
        stmt = insert(Users).values(
            first_name=first_name,
            last_name=last_name,
            patronymic=patronymic,
            username=username,
            role=role,
            hashed_password=hashed_password,
        )
        await session.execute(stmt)
        await session.commit()


class Department(BaseModel):
    __tablename__ = "departments"

    name = Column(String, nullable=False)
    img_link: Mapped[str] = Column(String, nullable=True)
    parent_id = Column(Integer, ForeignKey("departments.id"), nullable=True)

    @classmethod
    async def get_all(cls, session: AsyncSession):
        stmt = select(cls)
        result = (await session.execute(stmt)).scalars()
        return result
