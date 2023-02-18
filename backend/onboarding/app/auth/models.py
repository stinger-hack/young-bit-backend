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
    score = Column(Integer, default=0)
    img_link: Mapped[str] = Column(
        String, nullable=True, default="https://storage.yandexcloud.net/onboarding/ffd38812bdf14692b59bb89d1023ffa4.png"
    )

    # 1: https://storage.yandexcloud.net/onboarding/f0a33aea1f9c4c78aa815085a7e43a37.png
    # 2: https://storage.yandexcloud.net/onboarding/e1e135b2e9e54ab5b0f67a826dada9c8.png
    # 3: https://storage.yandexcloud.net/onboarding/8d370b1dc48a441aab05205a71185663.png
    # 4: https://storage.yandexcloud.net/onboarding/d83c70f0d948417f9fcf2e23ead1f6d1.png
    # 5: https://storage.yandexcloud.net/onboarding/a611efc7a2f44c9cb8243b30a37b56ad.png
    # 6: https://storage.yandexcloud.net/onboarding/1837703c9f92462c85b0955d0f2fbf1d.png

    card_map = {
        0: [
            "https://storage.yandexcloud.net/onboarding/f0a33aea1f9c4c78aa815085a7e43a37.png",
            "https://storage.yandexcloud.net/onboarding/e1e135b2e9e54ab5b0f67a826dada9c8.png",
            "https://storage.yandexcloud.net/onboarding/a611efc7a2f44c9cb8243b30a37b56ad.png",
            "https://storage.yandexcloud.net/onboarding/1837703c9f92462c85b0955d0f2fbf1d.png",
        ],
        1: [
            "https://storage.yandexcloud.net/onboarding/8d370b1dc48a441aab05205a71185663.png",
            "https://storage.yandexcloud.net/onboarding/a611efc7a2f44c9cb8243b30a37b56ad.png",
            "https://storage.yandexcloud.net/onboarding/f0a33aea1f9c4c78aa815085a7e43a37.png",
        ],
        2: [
            "https://storage.yandexcloud.net/onboarding/f0a33aea1f9c4c78aa815085a7e43a37.png",
        ],
        3: [
            "https://storage.yandexcloud.net/onboarding/f0a33aea1f9c4c78aa815085a7e43a37.png",
            "https://storage.yandexcloud.net/onboarding/1837703c9f92462c85b0955d0f2fbf1d.png",
        ],
        4: [
            "https://storage.yandexcloud.net/onboarding/f0a33aea1f9c4c78aa815085a7e43a37.png",
            "https://storage.yandexcloud.net/onboarding/e1e135b2e9e54ab5b0f67a826dada9c8.png",
            "https://storage.yandexcloud.net/onboarding/8d370b1dc48a441aab05205a71185663.png",
            "https://storage.yandexcloud.net/onboarding/d83c70f0d948417f9fcf2e23ead1f6d1.png",
            "https://storage.yandexcloud.net/onboarding/a611efc7a2f44c9cb8243b30a37b56ad.png",
            "https://storage.yandexcloud.net/onboarding/1837703c9f92462c85b0955d0f2fbf1d.png",
        ],
        5: [
            "https://storage.yandexcloud.net/onboarding/d83c70f0d948417f9fcf2e23ead1f6d1.png",
            "https://storage.yandexcloud.net/onboarding/e1e135b2e9e54ab5b0f67a826dada9c8.png",
        ],
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
