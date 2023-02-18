from enum import StrEnum


class NewsTypeEnum(StrEnum):
    FORMAL = "FORMAL"
    INFORMAL = "INFORMAL"
    INITIATIVE = "INITIATIVE"


class ActionType(StrEnum):
    LIKE = "LIKE"
    DISLIKE = "DISLIKE"
    COMMENT = "COMMENT"


class UserRoleEnum(StrEnum):
    EMPLOYEE = "EMPLOYEE"
    HR = "HR"
    ADMIN = "ADMIN"


class TaskTypeEnum(StrEnum):
    INDIVIDUAL = "INDIVIDUAL"
    DEPARTAMENT = "DEPARTAMENT"


class TaskStatusEnum(StrEnum):
    TO_DO = "TO_DO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"