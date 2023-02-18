from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from onboarding.app.auth.models import Users
from .views import CreateDepartmentTask, CreateIndividualTask, TaskView, TaskPayload
from .models import DepartmentTask, IndividualTask, Prize
from onboarding.auth.oauth2 import get_current_user
from onboarding.db import get_session
from onboarding.protocol import Response
from onboarding.enums import TaskTypeEnum

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.get("/tasks", response_model=Response[TaskView])
async def get_news(
    task_type: TaskTypeEnum, user: Users = Depends(get_current_user), session: AsyncSession = Depends(get_session)
):
    if task_type == TaskTypeEnum.INDIVIDUAL:
        result = await IndividualTask.get_by_user_id(user_id=user.id, session=session)
    elif task_type == TaskTypeEnum.DEPARTAMENT:
        user = await Users.get_by_id(user_id=user.id, session=session)
        result = await DepartmentTask.get_by_department_id(department_id=user.department_id, session=session)

    # TODO: to real data
    return Response(
        body=TaskView(tasks_count=18, tasks_finished=12, tasks=[TaskPayload.from_orm(item) for item in result])
    )


@router.post("/tasks/department", response_model=Response)
async def create_department_task(body: CreateDepartmentTask, session: AsyncSession = Depends(get_session)):
    await DepartmentTask.insert_data(
        title=body.title,
        description=body.description,
        img_link=body.img_link,
        cost=body.cost,
        department_id=body.department_id,
        session=session,
    )
    return Response()


@router.post("/tasks/individual", response_model=Response)
async def create_individual_task(body: CreateIndividualTask, session: AsyncSession = Depends(get_session)):
    await IndividualTask.insert_data(
        title=body.title,
        description=body.description,
        img_link=body.img_link,
        cost=body.cost,
        user_id=body.user_id,
        session=session,
    )
    return Response()


@router.get("/shop")
async def get_shop_prizes(session: AsyncSession = Depends(get_session)):
    result = await Prize.get_all(session=session)
    return Response(body=list(result))
