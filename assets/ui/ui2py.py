import os

def convert_ui_to_py(ui_file_path, py_file_path, qt_version):
    """
    使用 compileUi 函数将 .ui 文件转换为 .py 文件
    :param ui_file_path: .ui 文件的路径
    :param py_file_path: 生成的 .py 文件的路径
    :param qt_version: Qt 版本，'qt5' 或 'qt6'
    """
    try:
        if qt_version == 'qt5':
            from PyQt5.uic import compileUi
            with open(py_file_path, 'w', encoding='utf-8') as py_file:
                with open(ui_file_path, 'r', encoding='utf-8') as ui_file:
                    compileUi(ui_file, py_file)
        elif qt_version == 'qt6':
            from PyQt6.uic import compileUi as compileUi6
            with open(py_file_path, 'w', encoding='utf-8') as py_file:
                with open(ui_file_path, 'r', encoding='utf-8') as ui_file:
                    compileUi6(ui_file, py_file)
        print(f"已成功将 {ui_file_path} 转换为 {py_file_path}")
    except Exception as e:
        print(f"转换 {ui_file_path} 为 {py_file_path} 时出错: {e}")


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

    # 假设当前目录下有 .ui 文件需要转换，这里获取当前目录
    current_dir = os.getcwd()

    if has_qt5 and has_qt6:
        # 创建 qt5 和 qt6 目录
        qt5_dir = os.path.join(current_dir, 'pyqt5ui')
        qt6_dir = os.path.join(current_dir, 'pyqt6ui')
        os.makedirs(qt5_dir, exist_ok=True)
        os.makedirs(qt6_dir, exist_ok=True)
        print(f"Qt5 文件夹已创建: {qt5_dir}")
        print(f"Qt6 文件夹已创建: {qt6_dir}")

        for root, dirs, files in os.walk(current_dir):
            for file in files:
                if file.endswith('.ui'):
                    ui_file_path = os.path.join(root, file)
                    # 生成 Qt5 的 .py 文件
                    py_file_path_qt5 = os.path.join(qt5_dir, os.path.relpath(root, current_dir), file[:-3] + '.py')
                    os.makedirs(os.path.dirname(py_file_path_qt5), exist_ok=True)
                    convert_ui_to_py(ui_file_path, py_file_path_qt5, 'qt5')
                    # 生成 Qt6 的 .py 文件
                    py_file_path_qt6 = os.path.join(qt6_dir, os.path.relpath(root, current_dir), file[:-3] + '.py')
                    os.makedirs(os.path.dirname(py_file_path_qt6), exist_ok=True)
                    convert_ui_to_py(ui_file_path, py_file_path_qt6, 'qt6')
    elif has_qt5:
        qt5_dir = os.path.join(current_dir, 'pyqt5ui')
        os.makedirs(qt5_dir, exist_ok=True)
        for root, dirs, files in os.walk(current_dir):
            for file in files:
                if file.endswith('.ui'):
                    ui_file_path = os.path.join(root, file)
                    # 生成 Qt5 的 .py 文件
                    py_file_path_qt5 = os.path.join(qt5_dir, os.path.relpath(root, current_dir), file[:-3] + '.py')
                    os.makedirs(os.path.dirname(py_file_path_qt5), exist_ok=True)
                    convert_ui_to_py(ui_file_path, py_file_path_qt5, 'qt5')
    elif has_qt6:
        qt6_dir = os.path.join(current_dir, 'pyqt6ui')
        os.makedirs(qt6_dir, exist_ok=True)
        for root, dirs, files in os.walk(current_dir):
            for file in files:
                if file.endswith('.ui'):
                    ui_file_path = os.path.join(root, file)
                    # 生成 Qt6 的 .py 文件
                    py_file_path_qt6 = os.path.join(qt6_dir, os.path.relpath(root, current_dir), file[:-3] + '.py')
                    os.makedirs(os.path.dirname(py_file_path_qt6), exist_ok=True)
                    convert_ui_to_py(ui_file_path, py_file_path_qt6, 'qt6')
    else:
        print("系统中未找到 Qt5 或 Qt6，请安装相应的库。")