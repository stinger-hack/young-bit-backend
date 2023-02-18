from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from onboarding.app.auth.models import Users
from .views import TaskView
from .models import DepartmentTask, IndividualTask
from onboarding.auth.oauth2 import get_current_user
from onboarding.db import get_session
from onboarding.protocol import Response
from onboarding.enums import TaskTypeEnum

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.get("/tasks", response_model=Response[list[TaskView]])
async def get_news(
    task_type: TaskTypeEnum, user: Users = Depends(get_current_user), session: AsyncSession = Depends(get_session)
):
    if task_type == TaskTypeEnum.INDIVIDUAL:
        result = await IndividualTask.get_by_user_id(user_id=user.id, session=session)
    elif task_type == TaskTypeEnum.DEPARTAMENT:
        user = await Users.get_by_id(user_id=user.id, session=session)
        result = await DepartmentTask.get_by_department_id(department_id=user.department_id, session=session)

    return Response(body=[TaskView.from_orm(item) for item in result])
