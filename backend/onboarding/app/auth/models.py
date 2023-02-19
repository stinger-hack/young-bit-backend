from typing import Self
from passlib.context import CryptContext
from sqlalchemy import Column, String, insert, select, Integer, ForeignKey
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped
from sqlalchemy import func

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
    score = Column(Integer, default=0)
    img_link: Mapped[str] = Column(
        String, nullable=True, default="https://storage.yandexcloud.net/onboarding/ffd38812bdf14692b59bb89d1023ffa4.png"
    )

    # 1: https://storage.yandexcloud.net/onboarding/4fdc37de68954f129c8a3f989e83e487.png
    # 2: https://storage.yandexcloud.net/onboarding/0c0405f124a94088a9f4fe8c4636c7aa.png
    # 3: https://storage.yandexcloud.net/onboarding/e8d5c01b5ceb439b8ab97e81448cd62a.png
    # 4: https://storage.yandexcloud.net/onboarding/7e885ca6825948f289a01668edabe0ab.png
    # 5: https://storage.yandexcloud.net/onboarding/afbe8de88bac43e283585a09a8664aba.png
    # 6: https://storage.yandexcloud.net/onboarding/afbe8de88bac43e283585a09a8664aba.png

    card_map = {
        0: [
            "https://storage.yandexcloud.net/onboarding/4fdc37de68954f129c8a3f989e83e487.png",
            "https://storage.yandexcloud.net/onboarding/0c0405f124a94088a9f4fe8c4636c7aa.png",
            "https://storage.yandexcloud.net/onboarding/afbe8de88bac43e283585a09a8664aba.png",
            "https://storage.yandexcloud.net/onboarding/e8d5c01b5ceb439b8ab97e81448cd62a.png",
        ],
        1: [
            "https://storage.yandexcloud.net/onboarding/e8d5c01b5ceb439b8ab97e81448cd62a.png",
            "https://storage.yandexcloud.net/onboarding/afbe8de88bac43e283585a09a8664aba.png",
            "https://storage.yandexcloud.net/onboarding/4fdc37de68954f129c8a3f989e83e487.png",
        ],
        2: [
            "https://storage.yandexcloud.net/onboarding/c07074c8ba124a3da803113ddbb60918.png",
            "https://storage.yandexcloud.net/onboarding/0c0405f124a94088a9f4fe8c4636c7aa.png",
            "https://storage.yandexcloud.net/onboarding/e8d5c01b5ceb439b8ab97e81448cd62a.png",
            "https://storage.yandexcloud.net/onboarding/7e885ca6825948f289a01668edabe0ab.png",
            "https://storage.yandexcloud.net/onboarding/afbe8de88bac43e283585a09a8664aba.png",
            "https://storage.yandexcloud.net/onboarding/afbe8de88bac43e283585a09a8664aba.png",
        ],
        3: [
            "https://storage.yandexcloud.net/onboarding/4fdc37de68954f129c8a3f989e83e487.png",
            "https://storage.yandexcloud.net/onboarding/afbe8de88bac43e283585a09a8664aba.png",
        ],
        4: [
            "https://storage.yandexcloud.net/onboarding/4fdc37de68954f129c8a3f989e83e487.png",
        ],
        5: [
            "https://storage.yandexcloud.net/onboarding/7e885ca6825948f289a01668edabe0ab.png",
            "https://storage.yandexcloud.net/onboarding/0c0405f124a94088a9f4fe8c4636c7aa.png",
        ],
    }

    theme_map = {
        1: "Спорт",
        2: "Игры",
        3: "Корейские сериалы",
        4: "IT",
        5: "Квантовая физика",
    }

    @classmethod
    async def get_random_user(cls, user_id: int, session: AsyncSession):
        stmt = select(cls).where(cls.id != user_id).order_by(func.random())
        result = (await session.execute(stmt)).scalars().first()
        return result

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
    async def get_by_fullname(first_name: str, last_name: str | None, session: AsyncSession):
        stmt = select(Users).where(Users.first_name == first_name)
        if last_name:
            stmt = stmt.where(Users.last_name == last_name)

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
