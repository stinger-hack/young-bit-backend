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
