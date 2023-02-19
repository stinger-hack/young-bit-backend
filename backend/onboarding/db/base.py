from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base

from onboarding.config import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,
    future=True,
    isolation_level="AUTOCOMMIT",
    pool_size=50,
    max_overflow=10,
    pool_timeout=30,
)

Base = declarative_base()
