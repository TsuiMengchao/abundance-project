import subprocess
import os
import datetime
from src.config.config import project_name, version

# 定义要打包的主Python文件（可根据实际情况修改文件名）
main_file = "main.py"

resources_path = "public"

# 获取当前日期，格式化为年、月、日
current_date = datetime.datetime.now().strftime("%Y.%m.%d")


def get_pyinstaller_config():
    return {
        # 是否生成一个目录（包含可执行文件、依赖等），True为生成目录，False为生成单个可执行文件
        "onedir": True,
        # 是否显示打包过程中的详细信息，True为显示详细信息，False为只显示关键信息
        "verbose": False,
        # 是否添加额外的运行时可搜索路径，是一个列表，例如['path1', 'path2']
        "paths": [],
        # 是否去除控制台窗口（仅适用于Windows，生成图形化无控制台的可执行文件），默认True，因为是Qt程序
        "noconsole": False,
        # 是否对Python字节码进行加密，True为加密，False为不加密
        "encrypt": False,
        # 打包后生成的可执行文件名称（不包含扩展名，添加版本号和日期）
        "name": project_name,
        # 是否收集所有依赖项（包括隐藏导入等），True为收集所有可能的依赖，False按常规收集
        "collect_all": False,
        # 是否只进行分析阶段（不实际生成可执行文件，可用于查看依赖分析情况），True为只分析，False为正常打包
        "analyse": False,
    }

import os
import shutil


def delete_directory_and_contents(directory_path):
    """
    删除指定目录及其子目录下的所有文件，并删除该目录本身
    :param directory_path: 要删除的目录的路径
    """
    for root, dirs, files in os.walk(directory_path, topdown=False):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                os.remove(file_path)
            except OSError as e:
                print(f"删除文件 {file_path} 时出错: {e}")
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            try:
                shutil.rmtree(dir_path)
            except OSError as e:
                print(f"删除目录 {dir_path} 时出错: {e}")
    try:
        os.rmdir(directory_path)
    except OSError as e:
        print(f"删除目录 {directory_path} 时出错: {e}")

import shutil
import os

def copy_directory_contents(source_dir, target_dir):
    """
    将源目录下的所有内容复制到目标目录

    参数:
    source_dir (str): 源目录的路径
    target_dir (str): 目标目录的路径
    """
    try:
        # 确保目标目录存在，如果不存在则创建
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        for root, dirs, files in os.walk(source_dir):
            # 计算目标路径下相对应的子目录路径
            relative_path = os.path.relpath(root, source_dir)
            target_sub_dir = os.path.join(target_dir, relative_path)

            # 创建目标子目录（如果不存在）
            if not os.path.exists(target_sub_dir):
                os.makedirs(target_sub_dir)

            for file in files:
                source_file = os.path.join(root, file)
                target_file = os.path.join(target_sub_dir, file)
                shutil.copy2(source_file, target_file)

        print("复制完成！")
    except Exception as e:
        print(f"复制过程出现错误: {e}")


def build_pyinstaller_args(config):
    args = ["pyinstaller"]
    if config["onedir"]:
        args.append("--onedir")
    if config["verbose"]:
        args.append("--verbose")
    for path in config["paths"]:
        args.extend(["--path", path])
    if config["noconsole"]:
        args.append("--noconsole")
    if config["encrypt"]:
        args.append("--encrypt")
    if config["name"]:
        args.extend(["--name", config["name"]])
    if config["collect_all"]:
        args.append("--collect-all")
    if config["analyse"]:
        args.append("--analyse")
    args.append(main_file)
    return args


config = get_pyinstaller_config()
args = build_pyinstaller_args(config)
# 获取生成的目录名（默认是和打包后的可执行文件名相同，添加了后缀的目录名）
dist_dir = os.path.join(os.getcwd(), "dist", config["name"])
resources_dir = os.path.join(os.getcwd(), resources_path)
# 重命名外层目录为 {project_name}-{version}-{current_date}
new_dist_dir = os.path.join(os.getcwd(), "dist", f"{project_name}-{version}-{current_date}")

try:
    delete_directory_and_contents(dist_dir)
    delete_directory_and_contents(new_dist_dir)
    # 执行pyinstaller命令
    subprocess.run(args, check=True)
    print("打包成功！")

    copy_directory_contents(resources_dir, dist_dir)

    if os.path.exists(dist_dir):
        # 重命名外层目录为 {project_name}-{version}-{current_date}
        new_dist_dir = os.path.join(os.getcwd(), "dist", f"{project_name}-{version}-{current_date}")
        os.rename(dist_dir, new_dist_dir)
except subprocess.CalledProcessError as e:
    print(f"打包过程出现错误: {e}")