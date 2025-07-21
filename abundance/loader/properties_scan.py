import os
import yaml
import json
import logging

from abundance.utils.path_utils import PathUtils, PathPreference

logger = logging.getLogger(__name__)

from typing import Union, List, Tuple, Dict, Any

from abundance.loader.PropertyLoader import PropertyLoader


class PropertiesScanner:
    """
    配置扫描器，用于通过注解方式扩展PropertyLoader的搜索路径
    """

    def __init__(
            self,
            location: str = None,
            name: str = None,
            prefix: str = None,
            file: str = None,
            locations: List[str] = None,
            names: List[str] = None,
            prefixes: List[str] = None,
            files: List[str] = None,
            base_location: str = None,
            base_locations: List[str] = None
    ):
        """
        初始化配置扫描器

        Args:
            location: 单个配置文件位置
            name: 单个配置文件名
            prefix: 单个配置文件后缀
            file: 单个完整配置文件路径
            locations: 配置文件位置列表
            names: 配置文件名列表
            prefixes: 配置文件后缀列表
            files: 完整配置文件路径列表
        """
        # 处理单个值参数
        self.locations = self._process_single_or_list(location, locations)
        self.names = self._process_single_or_list(name, names)
        self.prefixes = self._process_single_or_list(prefix, prefixes)
        self.files = self._process_single_or_list(file, files)
        self.base_locations = self._process_single_or_list(base_location, base_locations)

    def _process_single_or_list(self, single_value, list_value) -> List[Any]:
        """处理单个值或列表参数，统一转换为列表"""
        result = []
        if single_value is not None:
            result.append(single_value)
        if list_value is not None:
            result.extend(list_value)
        return PathUtils.auto_fill_resources_path(result, PathPreference.ALL)

    def __call__(self, cls):
        """
        类装饰器逻辑，扩展PropertyLoader的配置
        """
        # 扩展PropertyLoader的配置
        if self.locations:
            PropertyLoader.default_location.extend(self.locations)

        if self.names:
            PropertyLoader.default_name.extend(self.names)

        if self.prefixes:
            PropertyLoader.default_prefix.extend(self.prefixes)

        if self.files:
            PropertyLoader.file_list.extend(self.files)

        if self.base_locations:
            PropertyLoader.default_base_locations.extend(self.base_locations)

        return cls