import redis
import time
from typing import List, Dict, Optional, Set, Any
from collections import defaultdict


class RedisUtils:
    def __init__(self, host='localhost', port=6379, db=0, password=None):
        """
        初始化Redis连接
        :param host: Redis服务器地址，默认localhost
        :param port: Redis服务器端口，默认6379
        :param db: Redis数据库编号，默认0
        :param password: Redis连接密码，若无需密码则为None
        """
        self.redis_client = redis.Redis(host=host, port=port, db=db, password=password)

    def expire(self, key: str, time: int, time_unit: str = 'seconds') -> bool:
        """
        指定缓存失效时间
        :param key: 键
        :param time: 时间（根据time_unit指定的单位）
        :param time_unit: 时间单位，可选值为'seconds'（秒）、'minutes'（分钟）、'hours'（小时）等，默认'seconds'
        :return: 设置成功返回True，失败返回False
        """
        try:
            time_in_seconds = self._convert_time(time, time_unit)
            if time_in_seconds > 0:
                self.redis_client.expire(key, time_in_seconds)
            return True
        except redis.RedisError as e:
            print(f"Error setting expiration time: {e}")
            return False

    def get_expire(self, key: str) -> int:
        """
        根据key获取过期时间
        :param key: 键
        :return: 时间（秒），返回 -1 代表没有设置过期时间（即永久有效）
        """
        return self.redis_client.ttl(key)

    def scan(self, pattern: str) -> List[str]:
        """
        查找匹配key
        :param pattern: 匹配的模式
        :return: 匹配到的key列表
        """
        cursor = 0
        result = []
        while True:
            cursor, keys = self.redis_client.scan(cursor, match=pattern)
            result.extend([key.decode('utf-8') for key in keys])
            if cursor == 0:
                break
        return result

    def find_keys_for_page(self, pattern_key: str, page: int, size: int) -> List[str]:
        """
        分页查询key
        :param pattern_key: 匹配的模式key
        :param page: 页码
        :param size: 每页数目
        :return: 对应页的key列表
        """
        cursor = 0
        result = []
        tmp_index = 0
        from_index = page * size
        to_index = page * size + size
        while True:
            cursor, keys = self.redis_client.scan(cursor, match=pattern_key)
            for key in keys:
                key_str = key.decode('utf-8')
                if tmp_index >= from_index and tmp_index < to_index:
                    result.append(key_str)
                    tmp_index += 1
                    continue
                if tmp_index >= to_index:
                    break
                tmp_index += 1
            if cursor == 0:
                break
        return result

    def has_key(self, key: str) -> bool:
        """
        判断key是否存在
        :param key: 键
        :return: 存在返回True，不存在返回False
        """
        return self.redis_client.exists(key)

    def del_key(self, *keys: str):
        """
        删除缓存
        :param keys: 可以传一个值或多个
        """
        if keys:
            if len(keys) == 1:
                result = self.redis_client.delete(keys[0])
                print(f"删除缓存：{keys[0]}，结果：{result}")
            else:
                existing_keys = [key for key in keys if self.has_key(key)]
                count = self.redis_client.delete(*existing_keys)
                print(f"成功删除缓存：{existing_keys}")
                print(f"缓存删除数量：{count} 个")

    def scan_del(self, pattern: str):
        """
        批量模糊删除key
        :param pattern: 匹配的模式
        """
        cursor = 0
        while True:
            cursor, keys = self.redis_client.scan(cursor, match=pattern)
            if keys:
                self.redis_client.delete(*keys)
            if cursor == 0:
                break

    # ============================String=============================

    def get(self, key: str) -> Optional[Any]:
        """
        普通缓存获取
        :param key: 键
        :return: 值，如果键不存在则返回None
        """
        return self.redis_client.get(key)

    def multi_get(self, keys: List[str]) -> List[Optional[Any]]:
        """
        批量获取
        :param keys: 键列表
        :return: 对应的值列表，若某个键不存在则对应位置为None
        """
        results = self.redis_client.mget(keys)
        return [result if result is not None else None for result in results]

    def set(self, key: str, value: Any, time: int = -1, time_unit: str = 'seconds') -> bool:
        """
        普通缓存放入
        :param key: 键
        :param value: 值
        :param time: 时间（根据time_unit指定的单位），time小于等于0将设置无限期，默认 -1
        :param time_unit: 时间单位，默认'seconds'
        :return: 设置成功返回True，失败返回False
        """
        try:
            if time > 0:
                time_in_seconds = self._convert_time(time, time_unit)
                self.redis_client.setex(key, time_in_seconds, value)
            else:
                self.redis_client.set(key, value)
            return True
        except redis.RedisError as e:
            print(f"Error setting key-value: {e}")
            return False

    # ================================Map=================================

    def hget(self, key: str, item: str) -> Optional[Any]:
        """
        HashGet
        :param key: 键 不能为None
        :param item: 项 不能为None
        :return: 值，如果键或项不存在则返回None
        """
        return self.redis_client.hget(key, item)

    def hmget(self, key: str) -> Dict[str, Any]:
        """
        获取hashKey对应的所有键值
        :param key: 键
        :return: 对应的多个键值组成的字典
        """
        return {k.decode('utf-8'): v for k, v in self.redis_client.hgetall(key).items()}

    def hmset(self, key: str, mapping: Dict[str, Any], time: int = -1, time_unit: str = 'seconds') -> bool:
        """
        HashSet
        :param key: 键
        :param mapping: 对应多个键值的字典
        :param time: 时间（根据time_unit指定的单位），注意如果已存在的hash表有时间，这里将会替换原有的时间，默认 -1
        :param time_unit: 时间单位，默认'seconds'
        :return: 设置成功返回True，失败返回False
        """
        try:
            self.redis_client.hset(key, mapping)
            if time > 0:
                self.expire(key, time, time_unit)
            return True
        except redis.RedisError as e:
            print(f"Error setting hash values: {e}")
            return False

    def hset(self, key: str, item: str, value: Any, time: int = -1, time_unit: str = 'seconds') -> bool:
        """
        向一张hash表中放入数据，如果不存在将创建
        :param key: 键
        :param item: 项
        :param value: 值
        :param time: 时间（根据time_unit指定的单位），注意如果已存在的hash表有时间，这里将会替换原有的时间，默认 -1
        :param time_unit: 时间单位，默认'seconds'
        :return: 设置成功返回True，失败返回False
        """
        try:
            self.redis_client.hset(key, item, value)
            if time > 0:
                self.expire(key, time, time_unit)
            return True
        except redis.RedisError as e:
            print(f"Error setting hash value: {e}")
            return False

    def hdel(self, key: str, *items: str):
        """
        删除hash表中的值
        :param key: 键 不能为None
        :param items: 项 可以是多个，不能为None
        """
        self.redis_client.hdel(key, *items)

    def h_has_key(self, key: str, item: str) -> bool:
        """
        判断hash表中是否有该项的值
        :param key: 键 不能为None
        :param item: 项 不能为None
        :return: 存在返回True，不存在返回False
        """
        return self.redis_client.hexists(key, item)

    def hincr(self, key: str, item: str, by: float) -> float:
        """
        hash递增，如果不存在，就会创建一个并把新增后的值返回
        :param key: 键
        :param item: 项
        :param by: 要增加的值（大于0）
        :return: 递增后的结果值
        """
        return self.redis_client.hincrbyfloat(key, item, by)

    def hdecr(self, key: str, item: str, by: float) -> float:
        """
        hash递减
        :param key: 键
        :param item: 项
        :param by: 要减少的值（小于0）
        :return: 递减后的结果值
        """
        return self.redis_client.hincrbyfloat(key, item, -by)

    # ============================set=============================

    def sget(self, key: str) -> Set[Any]:
        """
        根据key获取Set中的所有值
        :param key: 键
        :return: Set集合中的所有元素，如果键不存在则返回None
        """
        result = self.redis_client.smembers(key)
        return set([elem.decode('utf-8') for elem in result]) if result else None

    def s_has_key(self, key: str, value: Any) -> bool:
        """
        根据value从一个set中查询，是否存在
        :param key: 键
        :param value: 值
        :return: 存在返回True，不存在返回False
        """
        return self.redis_client.sismember(key, value)

    def sset(self, key: str, *values: Any) -> int:
        """
        将数据放入set缓存
        :param key: 键
        :param values: 值 可以是多个
        :return: 成功添加的元素个数
        """
        return self.redis_client.sadd(key, *values)

    def sset_and_time(self, key: str, time: int, *values: Any) -> int:
        """
        将set数据放入缓存，并设置过期时间
        :param key: 键
        :param time: 时间（秒），注意这里将会替换原有的时间
        :param values: 值 可以是多个
        :return: 成功添加的元素个数
        """
        count = self.redis_client.sadd(key, *values)
        if time > 0:
            self.expire(key, time)
        return count

    def sget_set_size(self, key: str) -> int:
        """
        获取set缓存的长度
        :param key: 键
        :return: Set集合中元素的个数，如果键不存在则返回0
        """
        return self.redis_client.scard(key)

    def set_remove(self, key: str, *values: Any) -> int:
        """
        移除值为value的元素
        :param key: 键
        :param values: 值 可以是多个
        :return: 移除的元素个数
        """
        return self.redis_client.srem(key, *values)

    # ===============================list=================================

    def lget(self, key: str, start: int, end: int) -> List[Optional[Any]]:
        """
        获取list缓存的内容
        :param key: 键
        :param start: 开始位置
        :param end: 结束位置，0到 -1代表所有值
        :return: 对应区间内的元素列表，如果键不存在则返回None
        """
        result = self.redis_client.lrange(key, start, end)
        return [elem if elem is not None else None for elem in result]

    def lget_list_size(self, key: str) -> int:
        """
        获取list缓存的长度
        :param key: 键
        :return: List列表中元素的个数，如果键不存在则返回0
        """
        return self.redis_client.llen(key)

    def lget_index(self, key: str, index: int) -> Optional[Any]:
        """
        通过索引获取list中的值
        :param key: 键
        :param index: 索引，index>=0时，0表头，1第二个元素，依次类推；index<0时，-1表尾，-2倒数第二个元素，依次类推
        :return: 对应索引位置的元素，如果键不存在或者索引超出范围则返回None
        """
        try:
            return self.redis_client.lindex(key, index)
        except redis.RedisError as e:
            print(f"Error getting list index value: {e}")
            return None

    def lset(self, key: str, value: Any, time: int = -1) -> bool:
        """
        将list放入缓存
        :param key: 键
        :param value: 值
        :param time: 时间（秒），注意这里将会替换原有的时间，默认 -1
        :return: 设置成功返回True，失败返回False
        """
        try:
            self.redis_client.rpush(key, value)
            if time > 0:
                self.expire(key, time)
            return True
        except redis.RedisError as e:
            print(f"Error pushing value to list: {e}")
            return False

    def lset_list(self, key: str, values: List[Any], time: int = -1) -> bool:
        """
        将list放入缓存
        :param key: 键
        :param values: 值列表
        :param time: 时间（秒），注意这里将会替换原有的时间，默认 -1
        :return: 设置成功返回True，失败返回False
        """
        try:
            self.redis_client.rpush(key, *values)
            if time > 0:
                self.expire(key, time)
            return True
        except redis.RedisError as e:
            print(f"Error pushing list values to list: {e}")
            return False

    def lupdate_index(self, key: str, index: int, value: Any) -> bool:
        """
        根据索引修改list中的某条数据
        :param key: 键
        :param index: 索引
        :param value: 值
        :return: 修改成功返回True，失败返回False
        """
        try:
            self.redis_client.lset(key, index, value)
            return True
        except redis.RedisError as e:
            print(f"Error updating list index value: {e}")
            return False

    def lremove(self, key: str, count: int, value: Any) -> int:
        """
        移除N个值为value的元素
        :param key: 键
        :param count: 移除的个数
        :param value: 值
        :return: 实际移除的元素个数
        """
        return self.redis_client.lrem(key, count, value)

    def del_by_keys(self, prefix: str, ids: Set[int]):
        """
        根据前缀和一组id删除对应的缓存键
        :param prefix: 前缀
        :param ids: id集合
        """
        keys = [f"{prefix}{id}" for id in ids]
        existing_keys = [key for key in keys if self.has_key(key)]
        count = self.redis_client.delete(*existing_keys)
        print(f"成功删除缓存：{existing_keys}")
        print(f"缓存删除数量：{count} 个")

    @staticmethod
    def _convert_time(time: int, time_unit: str) -> int:
        """
        将时间根据指定单位转换为秒
        :param time: 时间值
        :param time_unit: 时间单位，如'seconds'、'minutes'、'hours'等
        :return: 转换后的秒数
        """
        units = {
            'seconds': 1,
            'minutes': 60,
            'hours': 3600,
            'days': 86400
        }
        if time_unit.lower() in units:
            return time * units[time_unit.lower()]
        raise ValueError(f"不支持的时间单位: {time_unit}")


if __name__ == "__main__":
    redis_utils = RedisUtils()  # 使用默认配置初始化RedisUtils实例，如有需要可传入具体参数

    # 测试设置普通缓存
    key = "test_key"
    value = "test_value"
    result_set = redis_utils.set(key, value, 60)  # 设置缓存有效期为60秒
    print(f"设置缓存结果: {result_set}")

    # 测试获取普通缓存
    result_get = redis_utils.get(key)
    print(f"获取缓存结果: {result_get}")

    # 测试设置哈希缓存
    hash_key = "test_hash_key"
    hash_map = {"field1": "value1", "field2": "value2"}
    result_hmset = redis_utils.hmset(hash_key, hash_map, 120)  # 设置有效期为120秒
    print(f"设置哈希缓存结果: {result_hmset}")

    # 测试获取哈希缓存中的某个值
    hash_item_value = redis_utils.hget(hash_key, "field1")
    print(f"获取哈希缓存中指定项的值: {hash_item_value}")

    # 测试判断key是否存在
    exists_result = redis_utils.has_key(key)
    print(f"判断key是否存在结果: {exists_result}")

    # 测试删除缓存
    redis_utils.del_key(key)
    exists_result_after_del = redis_utils.has_key(key)
    print(f"删除后判断key是否存在结果: {exists_result_after_del}")

    # 测试分页查询key（这里以简单的模式进行测试，实际可按具体业务场景调整模式）
    pattern_key = "test_*"
    page = 1
    size = 10
    page_keys = redis_utils.find_keys_for_page(pattern_key, page, size)
    print(f"分页查询到的keys: {page_keys}")

    # 测试设置缓存过期时间（使用不同时间单位示例）
    another_key = "another_test_key"
    redis_utils.set(another_key, "another_value")
    set_expire_result = redis_utils.expire(another_key, 2, "minutes")  # 设置过期时间为2分钟
    print(f"设置过期时间结果（2分钟）: {set_expire_result}")