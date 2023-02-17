from sqlalchemy.orm import sessionmaker

from onboarding.app.auth.models import *  # noqa
from onboarding.app.games.models import *  # noqa
from onboarding.app.news.models import *  # noqa

from .base import Base, engine


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def get_session() -> AsyncSession:
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session