from enum import Enum


class OperatorType(Enum):
    """
    操作人类别，对应Java版本中的OperatorType枚举
    """
    OTHER = 0
    MANAGE = 1
    MOBILE = 2