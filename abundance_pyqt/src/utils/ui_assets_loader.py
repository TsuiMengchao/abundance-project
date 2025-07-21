import logging
import os

from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QFontDatabase, QFont, QPixmap
from pyqt6_plugins.examplebuttonplugin import QtGui

from abundance_common.core.utils.ValidationUtil import ValidationUtil
from abundance_common.core.utils.file.FileUtils import FileUtils

logger = logging.getLogger(__name__)

class UiAssetsLoader:
    @staticmethod
    def load_font(form, font_file_path):
        if os.path.exists(font_file_path):
            font_id = QFontDatabase.addApplicationFont(font_file_path)
            if font_id != -1:
                font_families = QFontDatabase.applicationFontFamilies(font_id)
                if font_families:
                    font = font_families[0]
                    form.setFont(QFont(font))
                    logger.info(f"成功设置字体为 {font}")
                else:
                    logger.error(f"虽然成功加载字体文件 {font_file_path}，但无法获取有效的字体家族名称，不能设置字体")
            else:
                logger.error(f"无法加载字体文件 {font_file_path}，可能是文件格式不支持或文件损坏")
        else:
            logger.error(f"字体文件 {font_file_path} 不存在，无法设置字体")

    @staticmethod
    def load_qss(form, qss_file_path):
        if os.path.exists(qss_file_path):
            with open(qss_file_path, encoding='utf-8') as file:
                qss = file.readlines()
                qss = ''.join(qss).strip('\n')
            form.setStyleSheet(qss)
        else:
            logger.error(f"样式表文件 {qss_file_path} 不存在，无法设置样式")

    @staticmethod
    def load_icon(form, icon_file_path):
        if os.path.exists(icon_file_path):
            form.setWindowIcon(QtGui.QIcon(icon_file_path))
        else:
            logger.error(f"图标文件 {icon_file_path} 不存在，无法设置图标")

    @staticmethod
    def load_pixmap(form, pixmap_file_path):
        pixmap = QPixmap(pixmap_file_path)
        # 将 QPixmap 实例设置到 QLabel 中
        form.setPixmap(pixmap)
        # 调整 QLabel 的大小以适应图片的大小
        form.setScaledContents(True)


    @staticmethod
    def load_html(form, html, zoom=None, loaded=None):
        if ValidationUtil.is_url(html):
            form.load(QUrl(html))
        elif ValidationUtil.is_file_path(html):
            form.setHtml(FileUtils.read_file_as_text(html))
        else:
            form.setHtml(html)

        if zoom: form.setZoomFactor(zoom)
        if loaded: form.loadFinished.connect(loaded)