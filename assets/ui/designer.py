import os
import platform
import sys


def check_and_start_designer(qt_version):
    system = platform.system()
    # 获取虚拟环境的根目录
    venv_base = sys.prefix

    if qt_version == 5:
        if system == "Windows":
            designer_path = os.path.join(venv_base, "Lib", "site-packages", "qt5_applications", "Qt", "bin", "designer.exe")
        elif system == "Linux":
            designer_path = os.path.join(venv_base, "bin", "designer-qt5")
        elif system == "Darwin":
            # 这里的 5.x.x 需替换为你实际安装的 Qt5 版本号
            designer_path = os.path.join(venv_base, "Qt", "5.x.x", "clang_64", "bin", "Designer.app", "Contents", "MacOS", "Designer")
        else:
            raise Exception("不支持的操作系统。")
    elif qt_version == 6:
        if system == "Windows":
            designer_path = os.path.join(venv_base, "Lib", "site-packages", "qt6_applications", "Qt", "bin", "designer.exe")
        elif system == "Linux":
            designer_path = os.path.join(venv_base, "bin", "designer-qt6")
        elif system == "Darwin":
            # 这里的 6.x.x 需替换为你实际安装的 Qt6 版本号
            designer_path = os.path.join(venv_base, "Qt", "6.x.x", "clang_64", "bin", "Designer.app", "Contents", "MacOS", "Designer")
        else:
            print("不支持的操作系统。")
            return False

    if os.path.exists(designer_path):
        os.system(f'"{designer_path}"')
        return True
    return False


if __name__ == "__main__":
    if not check_and_start_designer(5):
        if not check_and_start_designer(6):
            print("未找到 Qt5 或 Qt6 的 Designer，请检查安装情况。")
        else:
            print("已打开 Qt6 的 Designer")
    else:
        print("已打开 Qt5 的 Designer")