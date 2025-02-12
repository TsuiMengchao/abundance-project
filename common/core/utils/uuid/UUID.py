import hashlib
import binascii
import random


class UUID:
    def __init__(self, mostSigBits, leastSigBits):
        """
        使用指定的最高和最低有效位初始化UUID对象
        """
        self.mostSigBits = mostSigBits
        self.leastSigBits = leastSigBits

    @staticmethod
    def fastUUID():
        """
        获取类型4（伪随机生成的）UUID的静态工厂方法，对应Java版本中的fastUUID方法
        """
        return UUID.randomUUID(False)

    @staticmethod
    def randomUUID(isSecure = True):
        """
        获取类型4（伪随机生成的）UUID的静态工厂方法，根据是否使用加密强伪随机数生成器来生成UUID
        """
        if isSecure:
            random_bytes = bytearray(16)
            random_generator = random.SystemRandom()
            for i in range(len(random_bytes)):
                random_bytes[i] = random_generator.getrandbits(8)
            random_bytes[6] &= 0x0F  # clear version
            random_bytes[6] |= 0x40  # set to version 4
            random_bytes[8] &= 0x3F  # clear variant
            random_bytes[8] |= 0x80  # set to IETF variant

            return UUID._from_bytes(random_bytes)
        else:
            random_bytes = bytearray(random.getrandbits(8) for _ in range(16))

            random_bytes[6] &= 0x0F  # clear version
            random_bytes[6] |= 0x40  # set to version 4
            random_bytes[8] &= 0x3F  # clear variant
            random_bytes[8] |= 0x80  # set to IETF variant

            return UUID._from_bytes(random_bytes)

    @staticmethod
    def nameUUIDFromBytes(name):
        """
        根据指定的字节数组获取类型3（基于名称的）UUID的静态工厂方法，对应Java版本中的nameUUIDFromBytes方法
        """
        md5_hash = hashlib.md5(name)
        md5_bytes = bytearray(md5_hash.digest())  # 将bytes类型转换为bytearray类型，使其可变
        md5_bytes[6] &= 0x0F  # clear version
        md5_bytes[6] |= 0x30  # set to version 3
        md5_bytes[8] &= 0x3F  # clear variant
        md5_bytes[8] |= 0x80  # set to IETF variant

        # 如果后续需要以bytes类型返回，可再转换回bytes类型，此处根据具体需求来定，这里先转换回去方便后续统一处理
        md5_bytes = bytes(md5_bytes)
        return UUID._from_bytes(md5_bytes)

    @staticmethod
    def fromString(name):
        """
        根据字符串标准表示形式创建UUID对象，对应Java版本中的fromString方法
        """
        components = name.split('-')
        if len(components)!= 5:
            raise ValueError("Invalid UUID string: " + name)

        mostSigBits = int(components[0], 16)
        mostSigBits <<= 16
        mostSigBits |= int(components[1], 16)
        mostSigBits <<= 16
        mostSigBits |= int(components[2], 16)

        leastSigBits = int(components[3], 16)
        leastSigBits <<= 48
        leastSigBits |= int(components[4], 16)

        return UUID(mostSigBits, leastSigBits)

    def getLeastSignificantBits(self):
        """
        返回此UUID的128位值中的最低有效64位，对应Java版本中的getLeastSignificantBits方法
        """
        return self.leastSigBits

    def getMostSignificantBits(self):
        """
        返回此UUID的128位值中的最高有效64位，对应Java版本中的getMostSignificantBits方法
        """
        return self.mostSigBits

    def version(self):
        """
        获取与此UUID相关联的版本号，对应Java版本中的version方法
        """
        return (self.mostSigBits >> 12) & 0x0F

    def variant(self):
        """
        获取与此UUID相关联的变体号，对应Java版本中的variant方法
        """
        return (self.leastSigBits >> 63) & 0x03

    def timestamp(self):
        """
        获取与此UUID相关联的时间戳值，若不是基于时间的UUID则抛出异常，对应Java版本中的timestamp方法
        """
        if self.version()!= 1:
            raise NotImplementedError("Not a time-based UUID")
        return ((self.mostSigBits & 0x0FFF) << 48 |
                ((self.mostSigBits >> 16) & 0x0FFFF) << 32 |
                self.mostSigBits >> 32)

    def clockSequence(self):
        """
        获取与此UUID相关联的时钟序列值，若不是基于时间的UUID则抛出异常，对应Java版本中的clockSequence方法
        """
        if self.version()!= 1:
            raise NotImplementedError("Not a time-based UUID")
        return (self.leastSigBits >> 48) & 0x3FFF

    def node(self):
        """
        获取与此UUID相关的节点值，若不是基于时间的UUID则抛出异常，对应Java版本中的node方法
        """
        if self.version()!= 1:
            raise NotImplementedError("Not a time-based UUID")
        return self.leastSigBits & 0x0000FFFFFFFFFFFF

    def __str__(self):
        """
        返回此UUID的字符串表现形式，默认格式，对应Java版本中的toString方法
        """
        return self.toString(False)

    def toString(self, isSimple):
        """
        返回此UUID的字符串表现形式，可指定是否为简单模式（不带'-'的UUID字符串），对应Java版本中的toString方法
        """
        builder = []
        # time_low
        builder.append(self._digits(self.mostSigBits >> 32, 8))
        if not isSimple:
            builder.append('-')
        # time_mid
        builder.append(self._digits(self.mostSigBits >> 16, 4))
        if not isSimple:
            builder.append('-')
        # time_high_and_version
        builder.append(self._digits(self.mostSigBits, 4))
        if not isSimple:
            builder.append('-')
        # variant_and_sequence
        builder.append(self._digits(self.leastSigBits >> 48, 4))
        if not isSimple:
            builder.append('-')
        # node
        builder.append(self._digits(self.leastSigBits, 12))

        return "".join(builder)

    def __hash__(self):
        """
        返回此UUID的哈希码，对应Java版本中的hashCode方法
        """
        hilo = self.mostSigBits ^ self.leastSigBits
        return hash((hilo >> 32, hilo & 0xFFFFFFFF))

    def __eq__(self, other):
        """
        比较此UUID对象与另一个对象是否相等，对应Java版本中的equals方法
        """
        if other is None or not isinstance(other, UUID):
            return False
        return self.mostSigBits == other.mostSigBits and self.leastSigBits == other.leastSigBits

    def __lt__(self, other):
        """
        比较此UUID与另一个UUID的大小关系，用于排序等操作
        """
        if self.mostSigBits < other.mostSigBits:
            return True
        elif self.mostSigBits > other.mostSigBits:
            return False
        return self.leastSigBits < other.leastSigBits

    def __le__(self, other):
        """
        比较此UUID与另一个UUID的大小关系，用于排序等操作
        """
        return self < other or self == other

    def __gt__(self, other):
        """
        比较此UUID与另一个UUID的大小关系，用于排序等操作
        """
        return not self <= other

    def __ge__(self, other):
        """
        比较此UUID与另一个UUID的大小关系，用于排序等操作
        """
        return not self < other

    @staticmethod
    def _from_bytes(data):
        """
        根据字节数组创建UUID对象的私有辅助方法
        """
        assert len(data) == 16
        mostSigBits = 0
        leastSigBits = 0
        for i in range(8):
            mostSigBits = (mostSigBits << 8) | data[i]
        for i in range(8, 16):
            leastSigBits = (leastSigBits << 8) | data[i]
        return UUID(mostSigBits, leastSigBits)

    @staticmethod
    def _digits(val, digits):
        """
        返回指定数字对应的十六进制值的私有辅助方法，对应Java版本中的digits方法
        """
        hi = 1 << (digits * 4)
        hex_str = hex(hi | (val & (hi - 1)))[2:].zfill(digits)
        return hex_str

if __name__ == "__main__":
    # 测试randomUUID方法
    uuid_random = UUID.randomUUID()
    print(f"randomUUID方法生成的UUID: {uuid_random}")

    # 测试fastUUID方法
    uuid_fast = UUID.fastUUID()
    print(f"fastUUID方法生成的UUID: {uuid_fast}")

    # 测试nameUUIDFromBytes方法
    name_bytes = b"test_name"
    uuid_name = UUID.nameUUIDFromBytes(name_bytes)
    print(f"nameUUIDFromBytes方法生成的UUID: {uuid_name}")

    # 测试fromString方法
    uuid_str = "123e4567-e89b-12d3-a456-426655440000"
    try:
        uuid_from_str = UUID.fromString(uuid_str)
        print(f"fromString方法解析UUID字符串生成的UUID: {uuid_from_str}")
    except ValueError as e:
        print(f"fromString方法测试失败，错误信息: {e}")

    # 测试getLeastSignificantBits和getMostSignificantBits方法
    uuid = UUID.randomUUID()
    least_bits = uuid.getLeastSignificantBits()
    most_bits = uuid.getMostSignificantBits()
    print(f"getLeastSignificantBits方法获取的最低有效位: {least_bits}")
    print(f"getMostSignificantBits方法获取的最高有效位: {most_bits}")

    # 测试version方法
    version = uuid.version()
    print(f"version方法获取的版本号: {version}")

    # 测试variant方法
    variant = uuid.variant()
    print(f"variant方法获取的变体号: {variant}")

    # 测试timestamp方法（若不是基于时间的UUID会抛异常，这里仅示例调用）
    try:
        timestamp = uuid.timestamp()
        print(f"timestamp方法获取的时间戳: {timestamp}")
    except NotImplementedError as e:
        print(f"timestamp方法测试失败，错误信息: {e}")

    # 测试clockSequence方法（若不是基于时间的UUID会抛异常，这里仅示例调用）
    try:
        clock_sequence = uuid.clockSequence()
        print(f"clockSequence方法获取的时钟序列: {clock_sequence}")
    except NotImplementedError as e:
        print(f"clockSequence方法测试失败，错误信息: {e}")

    # 测试node方法（若不是基于时间的UUID会抛异常，这里仅示例调用）
    try:
        node_value = uuid.node()
        print(f"node方法获取的节点值: {node_value}")
    except NotImplementedError as e:
        print(f"node方法测试失败，错误信息: {e}")

    # 测试__str__和toString方法
    print(f"默认__str__方法返回的字符串表示: {uuid}")
    simple_uuid_str = uuid.toString(True)
    print(f"toString方法（简单模式）返回的字符串表示: {simple_uuid_str}")

    # 测试__hash__、__eq__等比较方法
    another_uuid = UUID.randomUUID()
    print(f"两个UUID对象是否相等（__eq__方法）: {uuid == another_uuid}")
    print(f"第一个UUID是否小于第二个UUID（__lt__方法）: {uuid < another_uuid}")