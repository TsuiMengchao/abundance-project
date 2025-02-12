import pickle
import json
from typing import Type


class FastJson2JsonRedisSerializer:
    DEFAULT_CHARSET = "utf-8"

    def __init__(self, clazz: Type):
        """
        初始化方法，接收要序列化和反序列化的对象类型，对应Java版本中的构造函数
        """
        self.clazz = clazz

    def serialize(self, t):
        """
        序列化方法，对应Java版本中的serialize方法
        """
        if t is None:
            return b""
        try:
            # 使用json.dumps将对象转换为JSON字符串，这里可以根据需要添加更多类似FastJSON的特性配置
            json_str = json.dumps(t, default=lambda o: o.__dict__)
            return json_str.encode(self.DEFAULT_CHARSET)
        except:
            raise SerializationException("序列化出现异常")

    def deserialize(self, bytes_data):
        """
        反序列化方法，对应Java版本中的deserialize方法
        """
        if bytes_data is None or len(bytes_data) == 0:
            return None
        try:
            # 先将字节数据转换为字符串
            str_data = bytes_data.decode(self.DEFAULT_CHARSET)
            # 使用json.loads将JSON字符串转换为对应的Python对象，这里可以根据需要添加类型检查等逻辑
            return json.loads(str_data, object_hook=lambda d: self.clazz(**d))
        except:
            raise SerializationException("反序列化出现异常")

class SerializationException(Exception):
    """
    自定义序列化异常类，用于在序列化和反序列化过程中出现问题时抛出异常，模拟Java中自定义异常的功能
    """
    def __init__(self, message="Serialization error occurred", *args, **kwargs):
        self.message = message
        super().__init__(self.message, *args, **kwargs)

    def __str__(self):
        return self.message