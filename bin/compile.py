import datetime
from pathlib import Path
import os
import shutil
import compileall
import platform
import fnmatch

from src.config.config import project_name, version

projectName = project_name  # 项目名
edition = f"cpython-{platform.python_version().split('.')[0]}{platform.python_version().split('.')[1]}"  # 版本号
target = "target"  # 输出路径
# 获取当前日期，格式化为年、月、日
current_date = datetime.datetime.now().strftime("%Y.%m.%d")

def get_ignored_items(gitignore_path):
    """
    读取.gitignore文件内容，返回需要忽略的文件和目录列表
    :param gitignore_path: .gitignore文件路径
    :return: 忽略的文件和目录列表
    """
    ignored_items = []
    if os.path.exists(gitignore_path):
        with open(gitignore_path, 'r') as f:
            for line in f.readlines():
                line = line.strip()
                if line and not line.startswith('#'):  # 忽略空行和注释行
                    ignored_items.append(line)
    return ignored_items

def remove_readonly(func, path, excinfo):
    os.chmod(path, 0o777)
    func(path)

def compile(root_path):
    """
    编译根目录下的包括子目录里的所有py文件成pyc文件到新的文件夹下，并根据.gitignore剔除不需要的目录和文件
    :param root_path: 需编译的目录
    :return:
    """
    root = Path(root_path)
    gitignore_path = root / '.gitignore'
    ignored_items = get_ignored_items(gitignore_path)

    # 手动添加 target 到忽略项
    ignored_items.append(target)

    # 先删除根目录下的pyc文件和__pycache__文件夹
    for src_file in root.rglob("*.pyc"):
        os.remove(src_file)
    for src_file in root.rglob("__pycache__"):
        shutil.rmtree(src_file, onerror=remove_readonly)

    dest = Path(root.parent / f"{target}/{projectName}-{version}-{edition}-{current_date}")  # 目标文件夹名称

    # 检查并删除目标目录
    if os.path.exists(dest):
        shutil.rmtree(dest, onerror=remove_readonly)

    # 只复制需要的文件和目录，排除.gitignore中指定的内容
    def ignore_files_and_dirs(directory, contents):
        ignored = set()
        for item in contents:
            item_path = os.path.relpath(os.path.join(directory, item), root)
            for pattern in ignored_items:
                if fnmatch.fnmatch(item_path, pattern) or fnmatch.fnmatch(item, pattern):
                    ignored.add(item)
                    break
        return ignored

    shutil.copytree(root, dest, ignore=ignore_files_and_dirs)

    compileall.compile_dir(root, force=True)  # 将项目下的py都编译成pyc文件

    for src_file in root.glob("**/*.pyc"):  # 遍历所有pyc文件
        relative_path = src_file.relative_to(root)  # pyc文件对应模块文件夹名称
        dest_folder = dest / str(relative_path.parent.parent)  # 在目标文件夹下创建同名模块文件夹
        os.makedirs(dest_folder, exist_ok=True)
        dest_file = dest_folder / (src_file.stem.rsplit(".", 1)[0] + src_file.suffix)  # 创建同名文件
        shutil.copyfile(src_file, dest_file)  # 将pyc文件复制到同名文件

    # 清除源py文件
    for src_file in dest.rglob("*.py"):
        os.remove(src_file)

if __name__ == '__main__':
    compile(root_path="./")
