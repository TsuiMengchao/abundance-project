class ServiceNameConstants:
    """
    服务名称，对应Java版本中的ServiceNameConstants类
    """
    # 认证服务的serviceid
    AUTH_SERVICE = "auth"
    # 系统模块的serviceid
    SYSTEM_SERVICE = "system"
    # 文件服务的serviceid
    FILE_SERVICE = "file"

if __name__ == "__main__":
    print(f"认证服务的serviceid常量: {ServiceNameConstants.AUTH_SERVICE}")
    print(f"系统模块的serviceid常量: {ServiceNameConstants.SYSTEM_SERVICE}")
    print(f"文件服务的serviceid常量: {ServiceNameConstants.FILE_SERVICE}")