import uuid


class IdUtils:
    @staticmethod
    def random_uuid():
        """
        获取随机UUID，对应Java版本中的randomUUID方法
        """
        return str(uuid.uuid4())

    @staticmethod
    def simple_uuid():
        """
        简化的UUID，去掉了横线，对应Java版本中的simpleUUID方法
        """
        return str(uuid.uuid4()).replace('-', '')

    @staticmethod
    def fast_uuid():
        """
        获取随机UUID，使用性能较好的方式生成（Python中可简单使用内置的uuid4方法，本身性能较优）
        对应Java版本中使用性能更好的ThreadLocalRandom生成UUID的功能
        """
        return str(uuid.uuid4())

    @staticmethod
    def fast_simple_uuid():
        """
        简化的UUID，去掉了横线，使用性能较好的方式生成
        对应Java版本中使用性能更好的ThreadLocalRandom生成UUID并去掉横线的功能
        """
        return str(uuid.uuid4()).replace('-', '')


if __name__ == "__main__":
    # 测试random_uuid方法
    random_uuid_result = IdUtils.random_uuid()
    print(f"random_uuid方法生成的UUID: {random_uuid_result}")

    # 测试simple_uuid方法
    simple_uuid_result = IdUtils.simple_uuid()
    print(f"simple_uuid方法生成的UUID: {simple_uuid_result}")

    # 测试fast_uuid方法
    fast_uuid_result = IdUtils.fast_uuid()
    print(f"fast_uuid方法生成的UUID: {fast_uuid_result}")

    # 测试fast_simple_uuid方法
    fast_simple_uuid_result = IdUtils.fast_simple_uuid()
    print(f"fast_simple_uuid方法生成的UUID: {fast_simple_uuid_result}")