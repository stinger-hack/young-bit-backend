from datetime import datetime
from onboarding.protocol import BaseModel


class TaskPayload(BaseModel):
    title: str
    description: str
    spent_time: int | None
    img_link: str | None
    cost: int | None
    created_at: datetime
    updated_at: datetime | None


class TaskView(BaseModel):
    tasks_count: int
    tasks_finished: int
    tasks: list[TaskPayload]


class CreateTaskRequest(BaseModel):
    title: str
    description: str
    img_link: str
    cost: int


class CreateDepartmentTask(CreateTaskRequest):
    department_id: int | None


class CreateIndividualTask(CreateTaskRequest):
    user_id: int | None
