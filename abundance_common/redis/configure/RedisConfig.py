import redis
from typing import Any

from abundance_common.redis.configure.FastJson2JsonRedisSerializer import FastJson2JsonRedisSerializer


class RedisConfig:
    def __init__(self, redis_connection):
        """
        初始化方法，接收Redis连接对象，用于后续配置相关序列化操作
        """
        self.redis_connection = redis_connection

    def configure_redis_template(self):
        """
        模拟配置RedisTemplate相关的序列化逻辑，对应Java代码中RedisTemplate的配置部分
        """
        # 使用简单的字符串序列化方式来处理Redis的key值（类似StringRedisSerializer）
        def key_serializer(key):
            return str(key).encode('utf-8') if key is not None else b""

        def key_deserializer(bytes_data):
            return bytes_data.decode('utf-8') if bytes_data is not None else None

        # 使用自定义的类似FastJson2JsonRedisSerializer的方式来处理Redis的value值
        def value_serializer(value):
            return FastJson2JsonRedisSerializer(Any).serialize(value)

        def value_deserializer(bytes_data):
            return FastJson2JsonRedisSerializer(Any).deserialize(bytes_data)

        # 配置Hash的key的序列化器（同样采用简单字符串序列化方式）
        def hash_key_serializer(hash_key):
            return str(hash_key).encode('utf-8') if hash_key is not None else b""

        def hash_key_deserializer(bytes_data):
            return bytes_data.decode('utf-8') if bytes_data is not None else None

        # 配置Hash的value的序列化器（使用自定义的类似FastJson2JsonRedisSerializer的方式）
        def hash_value_serializer(hash_value):
            return FastJson2JsonRedisSerializer(Any).serialize(hash_value)

        def hash_value_deserializer(bytes_data):
            return FastJson2JsonRedisSerializer(Any).deserialize(bytes_data)

        # 设置Redis连接对象的不同序列化器
        self.redis_connection.set_key_serializer(key_serializer)
        self.redis_connection.set_key_deserializer(key_deserializer)
        self.redis_connection.set_value_serializer(value_serializer)
        self.redis_connection.set_value_deserializer(value_deserializer)
        self.redis_connection.set_hash_key_serializer(hash_key_serializer)
        self.redis_connection.set_hash_value_serializer(hash_value_serializer)
        self.redis_connection.set_hash_value_deserializer(hash_value_deserializer)


if __name__ == "__main__":
    # 创建Redis连接对象（这里假设Redis服务在本地默认端口，根据实际情况修改连接参数）
    redis_conn = redis.Redis(host='localhost', port=6379, db=0)
    redis_config = RedisConfig(redis_conn)
    redis_config.configure_redis_template()

    # 以下是简单的示例操作，用于验证序列化器是否配置生效
    key = "test_key"
    value = {"name": "example", "age": 10}
    redis_conn.set(key, value)
    retrieved_value = redis_conn.get(key)
    print(retrieved_value)