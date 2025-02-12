import functools
import logging

from common.log.aspect.LogAspect import LogAspect  # 假设模块导入正确配置，能导入LogAspect类
from common.log.enums.BusinessType import BusinessType
from common.log.enums.OperatorType import OperatorType


class Log:
    logAspect = LogAspect()
    def __init__(self, title="", business_type=BusinessType.OTHER, operator_type=OperatorType.MANAGE,
                 is_save_request_data=True, is_save_response_data=True, exclude_param_names=()):
        self.title = title
        self.business_type = business_type
        self.operator_type = operator_type
        self.is_save_request_data = is_save_request_data
        self.is_save_response_data = is_save_response_data
        self.exclude_param_names = exclude_param_names

    def __call__(self, func):
        func.log_metadata = self


        # 使用LogAspect的装饰器自动包裹函数，实现切面逻辑
        func = self.logAspect.before(func)
        func = self.logAspect.after_returning(func)
        func = self.logAspect.after_throwing(func)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

if __name__ == '__main__':
    # 配置Python的logging模块基本信息（模拟Java中配置日志级别、格式等，这里简单配置输出到控制台）
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    @Log(title="示例模块", business_type=BusinessType.INSERT, exclude_param_names=["password"])
    def some_function(arg1, arg2):
        print(f"执行函数，参数为: {arg1}, {arg2}")
        return "函数执行结果"

    try:
        some_function("参数1", "arg2")
    except Exception as e:
        print(f"业务操作出现异常: {e}")