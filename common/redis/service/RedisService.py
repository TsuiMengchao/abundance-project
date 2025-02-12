import redis
import time
from typing import Any, List, Set, Collection, Optional, Iterator, Dict, Type
from common.redis.configure.FastJson2JsonRedisSerializer import FastJson2JsonRedisSerializer, SerializationException


class RedisService:
    def __init__(self, redis_connection):
        """
        初始化方法，接收Redis连接对象
        """
        self.redis_connection = redis_connection

    def set_cache_object(self, key: str, value: Any):
        """
        缓存基本的对象，对应Java版本中的setCacheObject方法（无超时时间设置的版本）
        """
        try:
            serializer = FastJson2JsonRedisSerializer(type(value))
            serialized_value = serializer.serialize(value)
            self.redis_connection.set(key, serialized_value)
        except SerializationException as e:
            print(f"设置缓存对象时序列化出错: {e}")

    def set_cache_object_with_timeout(self, key: str, value: Any, timeout: int, time_unit: str):
        """
        缓存基本的对象，并设置有效时间，对应Java版本中的setCacheObject方法（带超时时间设置的版本）
        """
        try:
            serializer = FastJson2JsonRedisSerializer(type(value))
            serialized_value = serializer.serialize(value)
            if time_unit.lower() == "seconds":
                self.redis_connection.setex(key, timeout, serialized_value)
            elif time_unit.lower() == "minutes":
                self.redis_connection.setex(key, timeout * 60, serialized_value)
            elif time_unit.lower() == "hours":
                self.redis_connection.setex(key, timeout * 3600, serialized_value)
            else:
                print(f"不支持的时间单位: {time_unit}")
                return
        except SerializationException as e:
            print(f"设置缓存对象时序列化出错: {e}")

    def expire(self, key: str, timeout: int, unit: str = "seconds"):
        """
        设置有效时间，对应Java版本中的expire方法
        """
        if unit.lower() == "seconds":
            return self.redis_connection.expire(key, timeout)
        elif unit.lower() == "minutes":
            return self.redis_connection.expire(key, timeout * 60)
        elif unit.lower() == "hours":
            return self.redis_connection.expire(key, timeout * 3600)
        else:
            print(f"不支持的时间单位: {unit}")
            return False

    def get_expire(self, key: str):
        """
        获取有效时间，对应Java版本中的getExpire方法
        """
        return self.redis_connection.ttl(key)

    def has_key(self, key: str):
        """
        判断 key是否存在，对应Java版本中的hasKey方法
        """
        return self.redis_connection.exists(key)

    def get_cache_object(self, key: str):
        """
        获得缓存的基本对象，对应Java版本中的getCacheObject方法
        """
        serialized_value = self.redis_connection.get(key)
        if serialized_value:
            try:
                serializer = FastJson2JsonRedisSerializer(Any)  # 这里假设获取的对象类型未知，可按需调整
                return serializer.deserialize(serialized_value)
            except SerializationException as e:
                print(f"获取缓存对象时反序列化出错: {e}")
        return None

    def delete_object(self, key: str):
        """
        删除单个对象，对应Java版本中的deleteObject方法（针对单个键的版本）
        """
        return self.redis_connection.delete(key) > 0

    def delete_object_collection(self, collection: Collection):
        """
        删除集合对象，对应Java版本中的deleteObject方法（针对集合键的版本）
        """
        keys = [self._serialize_value(key) for key in collection]
        return self.redis_connection.delete(*keys) > 0

    def set_cache_list(self, key: str, data_list: List[Any]):
        """
        缓存List数据，对应Java版本中的setCacheList方法
        """
        serializer = FastJson2JsonRedisSerializer(Any)  # 假设列表中元素类型未知，可按需调整
        serialized_list = [serializer.serialize(item) for item in data_list]
        return self.redis_connection.rpush(key, *serialized_list)

    def get_cache_list(self, key: str):
        """
        获得缓存的list对象，对应Java版本中的getCacheList方法
        """
        serialized_list = self.redis_connection.lrange(key, 0, -1)
        serializer = FastJson2JsonRedisSerializer(Any)  # 假设列表中元素类型未知，可按需调整
        return [serializer.deserialize(item) for item in serialized_list]

    def set_cache_set(self, key: str, data_set: Set[Any]):
        """
        缓存Set，对应Java版本中的setCacheSet方法
        """
        serializer = FastJson2JsonRedisSerializer(Any)  # 假设集合中元素类型未知，可按需调整
        serialized_set = [serializer.serialize(element) for element in data_set]
        for element in serialized_set:
            self.redis_connection.sadd(key, element)
        return serialized_set

    def get_cache_set(self, key: str):
        """
        获得缓存的set，对应Java版本中的getCacheSet方法
        """
        serialized_set = self.redis_connection.smembers(key)
        serializer = FastJson2JsonRedisSerializer(Any)  # 假设集合中元素类型未知，可按需调整
        return [serializer.deserialize(item) for item in serialized_set]

    def set_cache_map(self, key: str, data_map: Dict[str, Any]):
        """
        缓存Map，对应Java版本中的setCacheMap方法
        """
        for sub_key, value in data_map.items():
            serializer = FastJson2JsonRedisSerializer(type(value))
            serialized_value = serializer.serialize(value)
            self.redis_connection.hset(key, sub_key, serialized_value)

    def get_cache_map(self, key: str):
        """
        获得缓存的Map，对应Java版本中的getCacheMap方法
        """
        serialized_map = self.redis_connection.hgetall(key)
        result_map = {}
        for sub_key, serialized_value in serialized_map.items():
            try:
                serializer = FastJson2JsonRedisSerializer(Any)  # 假设值的类型未知，可按需调整
                result_map[sub_key.decode()] = serializer.deserialize(serialized_value)
            except SerializationException as e:
                print(f"获取缓存Map时反序列化出错: {e}")
        return result_map

    def set_cache_map_value(self, key: str, h_key: str, value: Any):
        """
        往Hash中存入数据，对应Java版本中的setCacheMapValue方法
        """
        serializer = FastJson2JsonRedisSerializer(type(value))
        serialized_value = serializer.serialize(value)
        self.redis_connection.hset(key, h_key, serialized_value)

    def get_cache_map_value(self, key: str, h_key: str):
        """
        获取Hash中的数据，对应Java版本中的getCacheMapValue方法
        """
        serialized_value = self.redis_connection.hget(key, h_key)
        if serialized_value:
            try:
                serializer = FastJson2JsonRedisSerializer(Any)  # 假设值的类型未知，可按需调整
                return serializer.deserialize(serialized_value)
            except SerializationException as e:
                print(f"获取缓存Map值时反序列化出错: {e}")
        return None

    def get_multi_cache_map_value(self, key: str, h_keys: Collection[object]):
        """
        获取多个Hash中的数据，对应Java版本中的getMultiCacheMapValue方法
        """
        serializer = FastJson2JsonRedisSerializer(Any)  # 假设值的类型未知，可按需调整
        serialized_h_keys = [self._serialize_value(h_key) for h_key in h_keys]
        serialized_values = self.redis_connection.hmget(key, serialized_h_keys)
        return [serializer.deserialize(value) if value else None for value in serialized_values]

    def delete_cache_map_value(self, key: str, h_key: str):
        """
        删除Hash中的某条数据，对应Java版本中的deleteCacheMapValue方法
        """
        return self.redis_connection.hdel(key, h_key) > 0

    def keys(self, pattern: str):
        """
        获得缓存的基本对象列表（根据前缀匹配键），对应Java版本中的keys方法
        """
        return [key.decode() for key in self.redis_connection.keys(pattern)]

    def _serialize_value(self, value: Any):
        """
        辅助方法，用于将值转换为可用于Redis操作的序列化形式，这里调用FastJson2JsonRedisSerializer进行序列化
        """
        serializer = FastJson2JsonRedisSerializer(type(value))
        return serializer.serialize(value)

    def _deserialize_value(self, serialized_value: bytes):
        """
        辅助方法，用于将从Redis获取的序列化数据反序列化为Python对象，这里调用FastJson2JsonRedisSerializer进行反序列化
        """
        serializer = FastJson2JsonRedisSerializer(Any)  # 假设类型未知，可按需调整
        return serializer.deserialize(serialized_value)