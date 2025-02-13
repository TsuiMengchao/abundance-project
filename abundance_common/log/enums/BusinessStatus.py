from enum import unique, Enum


class BusinessStatus(Enum):
    """
    操作状态，对应Java版本中的BusinessStatus枚举
    """
    SUCCESS = 0
    FAIL = 1