class CXConstant:
    """
    常用静态常量，模拟实现类似Java代码中ElConstant类的功能，用于定义一些常用的固定值
    """
    # win系统
    WIN = "win"
    # mac系统
    MAC = "mac"

if __name__ == '__main__':
    def check_system(system_type):
        if system_type == CXConstant.WIN:
            print("当前是Windows系统")
        elif system_type == CXConstant.MAC:
            print("当前是Mac系统")
        else:
            print("未知系统类型")


    system = "win"
    check_system(system)