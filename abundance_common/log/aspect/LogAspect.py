import time
import json
import traceback
from functools import wraps
import logging
import asyncio

from abundance_common.log.enums.BusinessStatus import BusinessStatus
from abundance_common.log.service.AsyncLogService import AsyncLogService  # 假设模块导入正确配置，能导入AsyncLogService类


class LogAspect:
    EXCLUDE_PROPERTIES = ["password", "oldPassword", "newPassword", "confirmPassword"]

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.time_threadlocal = None
        self.async_log_service = AsyncLogService()  # 实例化异步日志服务类

    def _handle_log(self, func, exception, json_result):
        """
        处理日志记录的核心私有方法，对应Java版本中handleLog方法的核心逻辑
        """
        try:
            if hasattr(func, "log_metadata"):
                log_metadata = func.log_metadata
                oper_log = {}
                oper_log["status"] = BusinessStatus.SUCCESS.value if exception is None else BusinessStatus.FAIL.value
                oper_log["oper_ip"] = "127.0.0.1"  # 模拟获取IP地址，实际需按真实逻辑获取
                oper_log["oper_url"] = ""  # 模拟获取请求URL，实际需按真实逻辑获取
                oper_log["method"] = f"{func.__qualname__}()"  # 获取函数名构建方法名信息
                oper_log["request_method"] = "GET"  # 这里模拟获取请求方法，实际按真实情况获取

                self._get_controller_method_description(func, log_metadata, oper_log, json_result)
                oper_log["cost_time"] = int((time.time() - self.time_threadlocal) * 1000)
                asyncio.run(self.async_log_service.save_sys_log(oper_log))  # 使用asyncio.run来运行异步保存日志方法
            else:
                return
        except Exception as exp:
            print(traceback.format_exc())
            self.logger.error(f"异常信息: {exp}")

    def _get_controller_method_description(self, func, log, oper_log, json_result):
        """
        获取注解中对方法的描述信息，对应Java版本中的getControllerMethodDescription方法
        """
        oper_log["business_type"] = log.business_type.value
        oper_log["title"] = log.title
        oper_log["operator_type"] = log.operator_type.value
        if log.is_save_request_data:
            self._set_request_value(func, oper_log, log.exclude_param_names)
        if log.is_save_response_data and json_result:
            oper_log["json_result"] = json.dumps(json_result)[:2000]

    def _set_request_value(self, func, oper_log, exclude_param_names):
        """
        获取请求的参数，放到log中，对应Java版本中的setRequestValue方法
        """
        request_method = oper_log["request_method"]
        if request_method in ["PUT", "POST", "DELETE"]:
            params = self._args_array_to_string(func.__code__.co_varnames, exclude_param_names)
            oper_log["oper_param"] = params[:2000]
        else:
            # 对于其他请求方法（如GET）的处理逻辑示例，这里简单返回空字符串，实际需按真实情况获取参数
            oper_log["oper_param"] = ""

    def _args_array_to_string(self, params_array, exclude_param_names):
        """
        参数拼装，对应Java版本中的argsArrayToString方法
        """
        params = ""
        for param in params_array:
            if param and param not in exclude_param_names:
                try:
                    json_obj = json.dumps(param)
                    params += json_obj + " "
                except:
                    pass
        return params.strip()

    def before(self, func):
        """
        处理请求前执行，模拟Java中@Before注解对应的逻辑，使用装饰器实现切面逻辑
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            self.time_threadlocal = time.time()
            return func(*args, **kwargs)
        return wrapper

    def after_returning(self, func):
        """
        处理完请求后执行，模拟Java中@AfterReturning注解对应的逻辑，使用装饰器实现切面逻辑
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            self._handle_log(func, None, result)
            return result
        return wrapper

    def after_throwing(self, func):
        """
        拦截异常操作，模拟Java中@AfterThrowing注解对应的逻辑，使用装饰器实现切面逻辑
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                self._handle_log(func, e, None)
                raise
            finally:
                pass
        return wrapper