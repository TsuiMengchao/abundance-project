class SecurityConstants:
    """
    权限相关通用常量，对应Java版本中的SecurityConstants类
    """
    # 用户ID字段
    DETAILS_USER_ID = "user_id"
    # 用户名字段
    DETAILS_USERNAME = "username"
    # 授权信息字段
    AUTHORIZATION_HEADER = "Authorization"
    # 请求来源
    FROM_SOURCE = "from-source"
    # 内部请求
    INNER = "inner"
    # 用户标识
    USER_KEY = "user_key"
    # 登录用户
    LOGIN_USER = "login_user"
    # 角色权限
    ROLE_PERMISSION = "role_permission"

if __name__ == "__main__":
    print(f"用户ID字段常量: {SecurityConstants.DETAILS_USER_ID}")
    print(f"用户名字段常量: {SecurityConstants.DETAILS_USERNAME}")
    print(f"授权信息字段常量: {SecurityConstants.AUTHORIZATION_HEADER}")
    print(f"请求来源常量: {SecurityConstants.FROM_SOURCE}")
    print(f"内部请求常量: {SecurityConstants.INNER}")
    print(f"用户标识常量: {SecurityConstants.USER_KEY}")
    print(f"登录用户常量: {SecurityConstants.LOGIN_USER}")
    print(f"角色权限常量: {SecurityConstants.ROLE_PERMISSION}")