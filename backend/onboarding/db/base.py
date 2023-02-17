from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base

from onboarding.config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=True, future=True)

Base = declarative_base()
