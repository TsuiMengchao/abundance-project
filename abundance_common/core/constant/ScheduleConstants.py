from enum import unique, Enum


class ScheduleConstants:
    """
    任务调度通用常量，对应Java版本中的ScheduleConstants类
    """
    # 任务类名
    TASK_CLASS_NAME = "TASK_CLASS_NAME"
    # 执行目标key
    TASK_PROPERTIES = "TASK_PROPERTIES"
    # 默认
    MISFIRE_DEFAULT = "0"
    # 立即触发执行
    MISFIRE_IGNORE_MISFIRES = "1"
    # 触发一次执行
    MISFIRE_FIRE_AND_PROCEED = "2"
    # 不触发立即执行
    MISFIRE_DO_NOTHING = "3"

@unique
class Status(Enum):
    """
    模拟Java中枚举类型，对应Java版本中的Status枚举
    """
    Normal = ("0")

    Pause = ("1")

    def __init__(self, value):
        self.value = str(value)


if __name__ == "__main__":
    print(f"任务类名常量: {ScheduleConstants.TASK_CLASS_NAME}")
    print(f"执行目标key常量: {ScheduleConstants.TASK_PROPERTIES}")
    print(f"默认常量: {ScheduleConstants.MISFIRE_DEFAULT}")
    print(f"立即触发执行常量: {ScheduleConstants.MISFIRE_IGNORE_MISFIRES}")
    print(f"触发一次执行常量: {ScheduleConstants.MISFIRE_FIRE_AND_PROCEED}")
    print(f"不触发立即执行常量: {ScheduleConstants.MISFIRE_DO_NOTHING}")
    print(f"正常状态对应值: {Status.Normal.value}")
    print(f"暂停状态对应值: {Status.Pause.value}")