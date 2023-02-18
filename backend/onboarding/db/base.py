from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base

from onboarding.config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=True, future=True, pool_size=100, max_overflow=0)

Base = declarative_base()
