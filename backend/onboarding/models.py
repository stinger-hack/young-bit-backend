from sqlalchemy import Column, Integer, DateTime, func

from .db.base import Base


class BaseModel(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True)


class BaseDatetimeModel(BaseModel):
    __abstract__ = True

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))
