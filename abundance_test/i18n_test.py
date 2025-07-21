import gettext
import logging
import os
from pathlib import Path

# 配置国际化
LOCALES_DIR = Path(__file__).parent / 'locales'
DEFAULT_LANGUAGE = 'en_US'

# 创建翻译器
t = gettext.translation(
    'messages',
    localedir=LOCALES_DIR,
    languages=[DEFAULT_LANGUAGE],
    fallback=True
)
_ = t.gettext

# 配置日志
logger = logging.getLogger('i18n_logger')
logger.setLevel(logging.INFO)

# 创建控制台处理器
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# 创建格式化器并添加到处理器
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)

# 将处理器添加到日志器
logger.addHandler(ch)


def set_language(lang: str) -> None:
    """设置当前语言"""
    global _, t
    try:
        t = gettext.translation(
            'messages',
            localedir=LOCALES_DIR,
            languages=[lang],
            fallback=True
        )
        _ = t.gettext
        logger.info(_("语言已设置为: %s"), lang)
    except Exception as e:
        logger.error(_("设置语言失败: %s"), str(e))


def main():
    # 示例日志
    logger.info(_("程序启动"))

    # 模拟操作
    try:
        # 尝试打开一个不存在的文件
        with open('non_existent_file.txt', 'r') as f:
            pass
    except FileNotFoundError:
        logger.error(_("文件未找到"))

    # 切换语言到中文
    set_language('zh_CN')

    # 再次记录相同的日志
    logger.info(_("程序启动"))

    try:
        # 再次尝试打开一个不存在的文件
        with open('non_existent_file.txt', 'r') as f:
            pass
    except FileNotFoundError:
        logger.error(_("文件未找到"))


if __name__ == "__main__":
    main()