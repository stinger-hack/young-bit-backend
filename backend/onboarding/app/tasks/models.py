from datetime import datetime
from sqlalchemy import Column, String, Integer, ForeignKey, select, insert, update, DateTime
from sqlalchemy.ext.asyncio import AsyncSession

from onboarding.models import BaseModel, BaseDatetimeModel
from onboarding.enums import TaskStatusEnum


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
    img_link = Column(String, nullable=True)
    cost = Column(Integer, nullable=True)
    done_time = Column(DateTime(timezone=True))
    status = Column(String(15), default=TaskStatusEnum.TO_DO)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    @classmethod
    async def insert_data(
        cls, title: str, description: str | None, img_link: str | None, cost: int, user_id: str, session: AsyncSession
    ):
        stmt = insert(cls).values(title=title, description=description, img_link=img_link, cost=cost, user_id=user_id)
        await session.execute(stmt)
        await session.commit()

    @classmethod
    async def get_by_user_id(cls, user_id: int, session: AsyncSession):
        stmt = select(cls).where(user_id == user_id)
        result = (await session.execute(stmt)).scalars()
        return result

    @classmethod
    async def change_status(cls, status: TaskStatusEnum, session: AsyncSession):
        if status == TaskStatusEnum.DONE:
            stmt = update(cls).values(status=status)
        else:
            stmt = update(cls).values(status=status, done_time=datetime.now())

        await session.execute(stmt)
        await session.commit()


class DepartmentTask(BaseDatetimeModel):
    __tablename__ = "department_tasks"

    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    spent_time = Column(Integer, nullable=True)
    img_link = Column(String, nullable=True)
    cost = Column(Integer, nullable=True)
    done_time = Column(DateTime(timezone=True))
    status = Column(String(15), default=TaskStatusEnum.TO_DO)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)

    @classmethod
    async def insert_data(
        cls,
        title: str,
        description: str | None,
        img_link: str | None,
        cost: int,
        department_id: str,
        session: AsyncSession,
    ):
        stmt = insert(cls).values(
            title=title, description=description, img_link=img_link, cost=cost, department_id=department_id
        )
        await session.execute(stmt)
        await session.commit()

    @classmethod
    async def change_status(cls, status: TaskStatusEnum, session: AsyncSession):
        if status == TaskStatusEnum.DONE:
            stmt = update(cls).values(status=status)
        else:
            stmt = update(cls).values(status=status, done_time=datetime.now())

        await session.execute(stmt)
        await session.commit()

    @classmethod
    async def get_by_department_id(cls, department_id: int, session: AsyncSession):
        stmt = select(cls).where(department_id == department_id)
        result = (await session.execute(stmt)).scalars()
        return result
