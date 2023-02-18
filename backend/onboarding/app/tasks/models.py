from sqlalchemy import Column, String, Integer, ForeignKey, select
from sqlalchemy.ext.asyncio import AsyncSession

from onboarding.models import BaseModel, BaseDatetimeModel


class Prize(BaseModel):
    __tablename__ = "prizes"

    title = Column(String, nullable=False)
    img_link = Column(String, nullable=True)
    cost = Column(Integer, nullable=False)


class IndividualTask(BaseDatetimeModel):
    __tablename__ = "individual_tasks"

    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    spent_time = Column(Integer, nullable=True)
    cost = Column(Integer, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    @classmethod
    async def get_by_user_id(cls, user_id: int, session: AsyncSession):
        stmt = select(cls).where(user_id == user_id)
        result = (await session.execute(stmt)).scalars()
        return result


class DepartmentTask(BaseDatetimeModel):
    __tablename__ = "department_tasks"

    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    spent_time = Column(Integer, nullable=True)
    cost = Column(Integer, nullable=True)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)

    @classmethod
    async def get_by_department_id(cls, department_id: int, session: AsyncSession):
        stmt = select(cls).where(department_id == department_id)
        result = (await session.execute(stmt)).scalars()
        return result

