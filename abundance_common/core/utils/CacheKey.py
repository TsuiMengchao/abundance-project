class CacheKey:
    """
    关于缓存的Key集合，模拟实现类似Java代码中CacheKey接口的功能
    """
    # 用户
    USER_ID = "user::id:"
    # 数据
    DATA_USER = "data::user:"
    # 菜单
    MENU_ID = "menu::id:"
    MENU_USER = "menu::user:"
    # 角色授权
    ROLE_AUTH = "role::auth:"
    # 角色信息
    ROLE_ID = "role::id:"
    # 部门
    DEPT_ID = "dept::id:"
    # 岗位
    JOB_ID = "job::id:"
    # 数据字典
    DICT_NAME = "dict::name:"

if __name__ == '__main__':

    # 使用示例，比如在某个函数中获取用户相关的缓存键
    def get_user_cache_key(user_id):
        return CacheKey.USER_ID + str(user_id)


    user_id = 123
    cache_key = get_user_cache_key(user_id)
    print(cache_key)