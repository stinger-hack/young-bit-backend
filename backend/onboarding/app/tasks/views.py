from onboarding.protocol import BaseModel


class TaskView(BaseModel):
    title: str
    description: str
    spent_time: int | None
    cost: int | None
