import os
import subprocess


def convert_qrc_to_py(qrc_file_path, py_file_path, qt_version):
    """
    将 .qrc 文件转换为 .py 文件
    :param qrc_file_path: .qrc 文件的路径
    :param py_file_path: 生成的 .py 文件的路径
    :param qt_version: Qt 版本，'qt5' 或 'qt6'
    """
    try:
        if qt_version == 'qt5':
            command = f'pyrcc5 {qrc_file_path} -o {py_file_path}'
        elif qt_version == 'qt6':
            command = f'pyrcc6 {qrc_file_path} -o {py_file_path}'
        else:
            print(f"不支持的 Qt 版本: {qt_version}")
            return

        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"已成功将 {qrc_file_path} 转换为 {py_file_path}")
        else:
            print(f"转换 {qrc_file_path} 为 {py_file_path} 时出错: {result.stderr}")
    except Exception as e:
        print(f"执行转换命令时出错: {e}")


if __name__ == "__main__":
    # 检查是否存在 Qt5 和 Qt6
    has_qt5 = False
    has_qt6 = False
    try:
        import PyQt5
        has_qt5 = True
    except ImportError:
        pass
    try:
        import PyQt6
        has_qt6 = True
    except ImportError:
        pass

    # 假设当前目录下有 .qrc 文件需要转换，这里获取当前目录
    current_dir = os.getcwd()

    if has_qt5 and has_qt6:
        # 创建 qt5 和 qt6 目录
        qt5_dir = os.path.join(current_dir, 'pyqt5ui')
        qt6_dir = os.path.join(current_dir, 'pyqt6ui')
        os.makedirs(qt5_dir, exist_ok=True)
        os.makedirs(qt6_dir, exist_ok=True)

        for root, dirs, files in os.walk(current_dir):
            for file in files:
                if file.endswith('.qrc'):
                    qrc_file_path = os.path.join(root, file)
                    # 生成 Qt5 的 .py 文件
                    py_file_path_qt5 = os.path.join(qt5_dir, file[:-4] + '.py')
                    convert_qrc_to_py(qrc_file_path, py_file_path_qt5, 'qt5')
                    # 生成 Qt6 的 .py 文件
                    py_file_path_qt6 = os.path.join(qt6_dir, file[:-4] + '.py')
                    convert_qrc_to_py(qrc_file_path, py_file_path_qt6, 'qt6')
    elif has_qt5:
        for root, dirs, files in os.walk(current_dir):
            for file in files:
                if file.endswith('.qrc'):
                    qrc_file_path = os.path.join(root, file)
                    py_file_path = os.path.join(root, file[:-4] + '.py')
                    convert_qrc_to_py(qrc_file_path, py_file_path, 'qt5')
    elif has_qt6:
        for root, dirs, files in os.walk(current_dir):
            for file in files:
                if file.endswith('.qrc'):
                    qrc_file_path = os.path.join(root, file)
                    py_file_path = os.path.join(root, file[:-4] + '.py')
                    convert_qrc_to_py(qrc_file_path, py_file_path, 'qt6')
    else:
        print("系统中未找到 Qt5 或 Qt6，请安装相应的库。")