import threading
from collections import defaultdict

from abundance_common.core.constant.SecurityConstants import SecurityConstants


class SecurityContextHolder:
    """
    获取当前线程变量中的 用户id、用户名称、Token等信息，对应Java版本中的SecurityContextHolder类
    """
    _local = threading.local()

    @staticmethod
    def set(key, value):
        """
        设置线程局部变量中的值，对应Java版本中的set方法
        """
        local_map = SecurityContextHolder.get_local_map()
        local_map[key] = value if value is not None else ""

    @staticmethod
    def get(key, clazz=None):
        """
        获取线程局部变量中指定键的值，若传入了类型参数clazz则尝试转换为指定类型返回（简单模拟，实际可能需要更严谨的类型转换逻辑），
        若未传入clazz则转换为字符串类型返回，对应Java版本中的不同参数的get方法
        """
        local_map = SecurityContextHolder.get_local_map()
        value = local_map.get(key, None)
        if clazz is None:
            return "" if value is None else str(value)
        return value

    @staticmethod
    def get_local_map():
        """
        获取当前线程的局部变量映射（字典形式），如果不存在则创建一个默认的空字典，对应Java版本中的getLocalMap方法
        """
        if not hasattr(SecurityContextHolder._local, "map"):
            SecurityContextHolder._local.map = defaultdict(lambda: None)
        return SecurityContextHolder._local.map

    @staticmethod
    def set_local_map(threadLocalMap):
        """
        设置当前线程的局部变量映射，对应Java版本中的setLocalMap方法
        """
        SecurityContextHolder._local.map = threadLocalMap

    @staticmethod
    def getUserId():
        """
        获取用户ID，从线程局部变量中获取对应键的值并转换为长整型（默认值为0），对应Java版本中的getUserId方法
        """
        return int(SecurityContextHolder.get(SecurityConstants.DETAILS_USER_ID) or 0)

    @staticmethod
    def setUserId(account):
        """
        设置用户ID，对应Java版本中的setUserId方法
        """
        SecurityContextHolder.set(SecurityConstants.DETAILS_USER_ID, account)

    @staticmethod
    def getUserName():
        """
        获取用户名，对应Java版本中的getUserName方法
        """
        return SecurityContextHolder.get(SecurityConstants.DETAILS_USERNAME)

    @staticmethod
    def setUserName(username):
        """
        设置用户名，对应Java版本中的setUserName方法
        """
        SecurityContextHolder.set(SecurityConstants.DETAILS_USERNAME, username)

    @staticmethod
    def getUserKey():
        """
        获取用户Key，对应Java版本中的getUserKey方法
        """
        return SecurityContextHolder.get(SecurityConstants.USER_KEY)

    @staticmethod
    def setUserKey(userKey):
        """
        设置用户Key，对应Java版本中的setUserKey方法
        """
        SecurityContextHolder.set(SecurityConstants.USER_KEY, userKey)

    @staticmethod
    def getPermission():
        """
        获取权限信息，对应Java版本中的getPermission方法
        """
        return SecurityContextHolder.get(SecurityConstants.ROLE_PERMISSION)

    @staticmethod
    def setPermission(permissions):
        """
        设置权限信息，对应Java版本中的setPermission方法
        """
        SecurityContextHolder.set(SecurityConstants.ROLE_PERMISSION, permissions)

    @staticmethod
    def remove():
        """
        移除当前线程的局部变量，对应Java版本中的remove方法
        """
        if hasattr(SecurityContextHolder._local, "map"):
            delattr(SecurityContextHolder._local, "map")


if __name__ == "__main__":
    # 示例使用
    SecurityContextHolder.set("test_key", "test_value")
    print(SecurityContextHolder.get("test_key"))
    print(SecurityContextHolder.getUserId())
    SecurityContextHolder.setUserId("123")
    print(SecurityContextHolder.getUserId())
    SecurityContextHolder.remove()