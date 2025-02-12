import os
import yaml
import json
import logging

logging.basicConfig(level=logging.ERROR)

class PropertyLoader:
    default_location = ['resources', 'resources/config', '/']
    default_name = ['application', 'bootstrap']
    default_prefix = ['yaml', 'yml', 'json']

    def __init__(self, environment):
        self.sources = None
        self.load()
        environment.property_sources = self.sources

    def load(self):
        file_list = []
        # 拼接所有可能配置文件列表
        for location in self.default_location:
            for name in self.default_name:
                for prefix in self.default_prefix:
                    file_path = os.path.join(location, f"{name}.{prefix}")
                    file_list.append(file_path)

        final_data = None
        # 遍历找到的文件列表
        for file in file_list:
            try:
                if os.path.exists(file):
                    logging.info(f"Loading {file}")
                    # 判断文件是否以 .yaml 或 .yml 结尾
                    if file.endswith(('.yaml', '.yml')):
                        # 以只读模式打开 .yaml 文件，并指定编码为 utf-8
                        with open(file, 'r', encoding='utf-8') as f:
                            # 使用 yaml.safe_load 方法解析 .yaml 文件内容
                            data = yaml.safe_load(f)
                    # 判断文件是否以 .json 结尾
                    elif file.endswith('.json'):
                        # 以只读模式打开 .json 文件，并指定编码为 utf-8
                        with open(file, 'r', encoding='utf-8') as f:
                            # 使用 json.load 方法解析 .json 文件内容
                            data = json.load(f)
                    else:
                        continue

                    if final_data is None:
                        # 如果最终数据还未初始化，将当前解析的数据赋值给最终数据
                        final_data = data
                    else:
                        # 若最终数据已存在，调用 merge_data 方法将当前解析的数据合并到最终数据中
                        final_data = self.merge_data(final_data, data)
            except (yaml.YAMLError, json.JSONDecodeError) as e:
                # 若解析 .yaml 或 .json 文件时出现错误，使用日志记录错误信息
                logging.error(f"解析文件 {file} 时出错: {e}")
            except Exception as e:
                # 若处理文件时出现其他未知错误，使用日志记录错误信息
                logging.error(f"处理文件 {file} 时发生未知错误: {e}")

        # 将最终合并后的数据赋值给类的实例变量 config_data
        self.sources = final_data

    def merge_data(self, data1, data2):
        """
        递归合并两个数据结构，这两个数据结构可以是字典或列表。
        当两个数据结构都是字典时，会递归合并相同键的值；当都是列表时，会将两个列表拼接起来；
        对于其他情况，直接返回第二个数据结构。

        :param data1: 第一个要合并的数据结构
        :param data2: 第二个要合并的数据结构
        :return: 合并后的数据结构
        """
        # 判断 data1 和 data2 是否都是字典类型
        if isinstance(data1, dict) and isinstance(data2, dict):
            # 复制 data1 到 result 中，避免修改原始的 data1
            result = data1.copy()
            # 遍历 data2 的键值对
            for key, value in data2.items():
                if key in result:
                    # 如果键已经存在于 result 中，递归调用 merge_data 方法合并对应的值
                    result[key] = self.merge_data(result[key], value)
                else:
                    # 如果键不存在于 result 中，直接将该键值对添加到 result 中
                    result[key] = value
            return result
        # 判断 data1 和 data2 是否都是列表类型
        elif isinstance(data1, list) and isinstance(data2, list):
            # 如果都是列表，将两个列表拼接起来并返回
            return data1 + data2
        # 对于其他情况，直接返回 data2
        return data2
