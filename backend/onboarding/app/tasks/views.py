from datetime import datetime
from onboarding.protocol import BaseModel


class TaskPayload(BaseModel):
    title: str
    description: str
    spent_time: int | None
    cost: int | None
    created_at: datetime
    updated_at: datetime | None


class TaskView(BaseModel):
    tasks_count: int
    tasks_finished: int
    tasks: list[TaskPayload]
