import os
from enum import Enum
from functools import lru_cache


class PathPreference(Enum):
    FIRST = 1  # 返回第一个找到的路径
    LONGEST = 2  # 返回最长的路径
    SHORTEST = 3  # 返回最短的路径
    ALL = 4  # 返回所有找到的路径


class PathUtils:
    def __init__(self):
        self.tmp_paths = {"resources:": ["resources/", ""]}

    @staticmethod
    def auto_fill_resources_path(data, preference=PathPreference.FIRST):
        if isinstance(data, str):
            if data.startswith(tuple(PathUtils().tmp_paths.keys())):
                for prefix in PathUtils().tmp_paths:
                    if data.startswith(prefix):
                        return PathUtils().get_resources_path(data, prefix, PathUtils().tmp_paths.get(prefix),
                                                              preference)
        elif isinstance(data, dict):
            new_data = {}
            for key, value in data.items():
                new_data[key] = PathUtils.auto_fill_resources_path(value, preference)
            return new_data
        elif isinstance(data, list):
            processed_items = [PathUtils.auto_fill_resources_path(item, preference) for item in data]
            # 如果需要展开列表且处理后的元素包含列表，则展开

            flat_items = []
            for item in processed_items:
                if isinstance(item, list):
                    flat_items.extend(item)
                else:
                    flat_items.append(item)
            return flat_items
        return data

    @staticmethod
    def get_resources_path(path, prefix, locations, preference=PathPreference.FIRST):
        """
        根据指定的偏好策略获取资源路径

        Args:
            path: 原始路径字符串
            prefix: 要替换的前缀
            locations: 可能的位置列表
            preference: 路径选择策略 (PathPreference 枚举)

        Returns:
            单个路径 (FIRST/LONGEST/SHORTEST) 或路径列表 (ALL)
        """
        # 收集所有存在的路径
        existing_paths = []
        for location in locations:
            real_path = path.replace(prefix, location, 1)
            if os.path.exists(real_path):
                existing_paths.append(real_path)

        # 如果没有找到任何路径，返回原始路径或空列表
        if not existing_paths:
            return path if preference != PathPreference.ALL else []

        # 根据偏好策略选择路径
        if preference == PathPreference.FIRST:
            return existing_paths[0]  # 返回第一个匹配的路径
        elif preference == PathPreference.LONGEST:
            return max(existing_paths, key=len)  # 返回最长的路径
        elif preference == PathPreference.SHORTEST:
            return min(existing_paths, key=len)  # 返回最短的路径
        elif preference == PathPreference.ALL:
            return existing_paths  # 返回所有匹配的路径
        else:
            return existing_paths[0]  # 默认返回第一个