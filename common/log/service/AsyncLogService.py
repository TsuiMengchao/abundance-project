import asyncio

from common.core.constant.SecurityConstants import SecurityConstants


class AsyncLogService:
    def __init__(self):
        # 这里简单模拟注入RemoteLogService，实际可能需要更合理的依赖管理方式
        # self.remote_log_service = RemoteLogService()
        pass

    async def save_sys_log(self, sys_oper_log):
        """
        模拟保存系统日志记录，对应Java版本中的saveSysLog方法，使用Python的asyncio实现异步功能
        """
        await asyncio.sleep(0)  # 这里简单模拟异步等待，实际可能是真实的异步操作耗时
        print(f"在这里调用日志保存方法，保存以下信息：{sys_oper_log}")
        # self.remote_log_service.save_log(sys_oper_log, SecurityConstants.INNER)

if __name__ == '__main__':
    if __name__ == "__main__":
        # 模拟SysOperLog数据结构，这里简单用字典表示（实际根据真实业务定义对应类）
        sys_oper_log = {
            "key": "value"
        }
        async_log_service = AsyncLogService()
        # 通过asyncio.run来运行异步函数
        asyncio.run(async_log_service.save_sys_log(sys_oper_log))