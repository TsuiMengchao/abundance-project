class Constants:
    """
    通用常量信息，对应Java版本中的Constants类
    """
    # UTF-8 字符集
    UTF8 = "UTF-8"
    # GBK 字符集
    GBK = "GBK"
    # www主域
    WWW = "www."
    # RMI 远程方法调用
    LOOKUP_RMI = "rmi:"
    # LDAP 远程方法调用
    LOOKUP_LDAP = "ldap:"
    # LDAPS 远程方法调用
    LOOKUP_LDAPS = "ldaps:"
    # http请求
    HTTP = "http://"
    # https请求
    HTTPS = "https://"
    # 成功标记
    SUCCESS = 200
    # 失败标记
    FAIL = 500
    # 登录成功状态
    LOGIN_SUCCESS_STATUS = "0"
    # 登录失败状态
    LOGIN_FAIL_STATUS = "1"
    # 登录成功
    LOGIN_SUCCESS = "Success"
    # 注销
    LOGOUT = "Logout"
    # 注册
    REGISTER = "Register"
    # 登录失败
    LOGIN_FAIL = "Error"
    # 当前记录起始索引
    PAGE_NUM = "pageNum"
    # 每页显示记录数
    PAGE_SIZE = "pageSize"
    # 排序列
    ORDER_BY_COLUMN = "orderByColumn"
    # 排序的方向 "desc" 或者 "asc".
    IS_ASC = "isAsc"
    # 验证码有效期（分钟）
    CAPTCHA_EXPIRATION = 2
    # 资源映射路径 前缀
    RESOURCE_PREFIX = "/profile"

if __name__ == "__main__":
    print(f"UTF-8 字符集常量: {Constants.UTF8}")
    print(f"GBK 字符集常量: {Constants.GBK}")
    print(f"www主域常量: {Constants.WWW}")
    print(f"RMI 远程方法调用常量: {Constants.LOOKUP_RMI}")
    print(f"LDAP 远程方法调用常量: {Constants.LOOKUP_LDAP}")
    print(f"LDAPS 远程方法调用常量: {Constants.LOOKUP_LDAPS}")
    print(f"http请求常量: {Constants.HTTP}")
    print(f"https请求常量: {Constants.HTTPS}")
    print(f"成功标记常量: {Constants.SUCCESS}")
    print(f"失败标记常量: {Constants.FAIL}")
    print(f"登录成功状态常量: {Constants.LOGIN_SUCCESS_STATUS}")
    print(f"登录失败状态常量: {Constants.LOGIN_FAIL_STATUS}")
    print(f"登录成功常量: {Constants.LOGIN_SUCCESS}")
    print(f"注销常量: {Constants.LOGOUT}")
    print(f"注册常量: {Constants.REGISTER}")
    print(f"登录失败常量: {Constants.LOGIN_FAIL}")
    print(f"当前记录起始索引常量: {Constants.PAGE_NUM}")
    print(f"每页显示记录数常量: {Constants.PAGE_SIZE}")
    print(f"排序列常量: {Constants.ORDER_BY_COLUMN}")
    print(f"排序方向常量: {Constants.IS_ASC}")
    print(f"验证码有效期（分钟）常量: {Constants.CAPTCHA_EXPIRATION}")
    print(f"资源映射路径 前缀常量: {Constants.RESOURCE_PREFIX}")