class CacheConstants:
    """
    缓存常量信息，对应Java版本中的CacheConstants类
    """
    # 缓存有效期，默认720（分钟）
    EXPIRATION = 720
    # 缓存刷新时间，默认120（分钟）
    REFRESH_TIME = 120
    # 密码最大错误次数
    PASSWORD_MAX_RETRY_COUNT = 5
    # 密码锁定时间，默认10（分钟）
    PASSWORD_LOCK_TIME = 10
    # 权限缓存前缀
    LOGIN_TOKEN_KEY = "login_tokens:"
    # 验证码 redis key
    CAPTCHA_CODE_KEY = "captcha_codes:"
    # 参数管理 cache key
    SYS_CONFIG_KEY = "sys_config:"
    # 字典管理 cache key
    SYS_DICT_KEY = "sys_dict:"
    # 登录账户密码错误次数 redis key
    PWD_ERR_CNT_KEY = "pwd_err_cnt:"
    # 登录IP黑名单 cache key
    SYS_LOGIN_BLACKIPLIST = SYS_CONFIG_KEY + "sys.login.blackIPList"

if __name__ == "__main__":
    print(f"缓存有效期: {CacheConstants.EXPIRATION} 分钟")
    print(f"缓存刷新时间: {CacheConstants.REFRESH_TIME} 分钟")
    print(f"密码最大错误次数: {CacheConstants.PASSWORD_MAX_RETRY_COUNT}")
    print(f"密码锁定时间: {CacheConstants.PASSWORD_LOCK_TIME} 分钟")
    print(f"权限缓存前缀: {CacheConstants.LOGIN_TOKEN_KEY}")
    print(f"验证码 redis key: {CacheConstants.CAPTCHA_CODE_KEY}")
    print(f"参数管理 cache key: {CacheConstants.SYS_CONFIG_KEY}")
    print(f"字典管理 cache key: {CacheConstants.SYS_DICT_KEY}")
    print(f"登录账户密码错误次数 redis key: {CacheConstants.PWD_ERR_CNT_KEY}")
    print(f"登录IP黑名单 cache key: {CacheConstants.SYS_LOGIN_BLACKIPLIST}")