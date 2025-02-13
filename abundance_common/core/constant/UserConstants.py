class UserConstants:
    """
    用户常量信息，对应Java版本中的UserConstants类
    """
    # 平台内系统用户的唯一标志
    SYS_USER = "SYS_USER"
    # 正常状态
    NORMAL = "0"
    # 异常状态
    EXCEPTION = "1"
    # 用户封禁状态
    USER_DISABLE = "1"
    # 角色正常状态
    ROLE_NORMAL = "0"
    # 角色封禁状态
    ROLE_DISABLE = "1"
    # 部门正常状态
    DEPT_NORMAL = "0"
    # 部门停用状态
    DEPT_DISABLE = "1"
    # 字典正常状态
    DICT_NORMAL = "0"
    # 是否为系统默认（是）
    YES = "Y"
    # 是否菜单外链（是）
    YES_FRAME = "0"
    # 是否菜单外链（否）
    NO_FRAME = "1"
    # 菜单类型（目录）
    TYPE_DIR = "M"
    # 菜单类型（菜单）
    TYPE_MENU = "C"
    # 菜单类型（按钮）
    TYPE_BUTTON = "F"
    # Layout组件标识
    LAYOUT = "Layout"
    # ParentView组件标识
    PARENT_VIEW = "ParentView"
    # InnerLink组件标识
    INNER_LINK = "InnerLink"
    # 校验是否唯一的返回标识
    UNIQUE = True
    NOT_UNIQUE = False
    # 用户名长度限制
    USERNAME_MIN_LENGTH = 2
    USERNAME_MAX_LENGTH = 20
    # 密码长度限制
    PASSWORD_MIN_LENGTH = 5
    PASSWORD_MAX_LENGTH = 20

if __name__ == "__main__":
    print(f"平台内系统用户的唯一标志常量: {UserConstants.SYS_USER}")
    print(f"正常状态常量: {UserConstants.NORMAL}")
    print(f"异常状态常量: {UserConstants.EXCEPTION}")
    print(f"用户封禁状态常量: {UserConstants.USER_DISABLE}")
    print(f"角色正常状态常量: {UserConstants.ROLE_NORMAL}")
    print(f"角色封禁状态常量: {UserConstants.ROLE_DISABLE}")
    print(f"部门正常状态常量: {UserConstants.DEPT_NORMAL}")
    print(f"部门停用状态常量: {UserConstants.DEPT_DISABLE}")
    print(f"字典正常状态常量: {UserConstants.DICT_NORMAL}")
    print(f"是否为系统默认（是）常量: {UserConstants.YES}")
    print(f"是否菜单外链（是）常量: {UserConstants.YES_FRAME}")
    print(f"是否菜单外链（否）常量: {UserConstants.NO_FRAME}")
    print(f"菜单类型（目录）常量: {UserConstants.TYPE_DIR}")
    print(f"菜单类型（菜单）常量: {UserConstants.TYPE_MENU}")
    print(f"菜单类型（按钮）常量: {UserConstants.TYPE_BUTTON}")
    print(f"Layout组件标识常量: {UserConstants.LAYOUT}")
    print(f"ParentView组件标识常量: {UserConstants.PARENT_VIEW}")
    print(f"InnerLink组件标识常量: {UserConstants.INNER_LINK}")
    print(f"校验是否唯一的返回标识（唯一）常量: {UserConstants.UNIQUE}")
    print(f"校验是否唯一的返回标识（不唯一）常量: {UserConstants.NOT_UNIQUE}")
    print(f"用户名长度限制（最小）常量: {UserConstants.USERNAME_MIN_LENGTH}")
    print(f"用户名长度限制（最大）常量: {UserConstants.USERNAME_MAX_LENGTH}")
    print(f"密码长度限制（最小）常量: {UserConstants.PASSWORD_MIN_LENGTH}")
    print(f"密码长度限制（最大）常量: {UserConstants.PASSWORD_MAX_LENGTH}")