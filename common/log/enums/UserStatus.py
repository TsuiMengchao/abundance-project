from enum import unique, Enum


@unique
class UserStatus(Enum):
    """
    模拟Java中的UserStatus枚举，以及实现类似的code唯一性验证逻辑（简单模拟）
    """
    OK = ("0", "正常")
    DISABLE = ("1", "停用")
    DELETED = ("2", "删除")

    def __init__(self, code, info):
        self.code = str(code)
        self.info = str(info)