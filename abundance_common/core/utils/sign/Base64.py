class Base64:
    BASELENGTH = 128
    LOOKUPLENGTH = 64
    TWENTYFOURBITGROUP = 24
    EIGHTBIT = 8
    SIXTEENBIT = 16
    FOURBYTE = 4
    SIGN = -128
    PAD = "="
    base64_alphabet = [-1] * BASELENGTH
    look_up_base64_alphabet = [""] * LOOKUPLENGTH

    @staticmethod
    def _init_alphabet():
        """
        初始化Base64编码字符映射表，类似Java代码中的静态初始化块功能
        """
        for i in range(ord('Z'), ord('A') - 1, -1):
            Base64.base64_alphabet[i] = i - ord('A')
        for i in range(ord('z'), ord('a') - 1, -1):
            Base64.base64_alphabet[i] = i - ord('a') + 26
        for i in range(ord('9'), ord('0') - 1, -1):
            Base64.base64_alphabet[i] = i - ord('0') + 52
        Base64.base64_alphabet[ord('+')] = 62
        Base64.base64_alphabet[ord('/')] = 63

        for i in range(26):
            Base64.look_up_base64_alphabet[i] = chr(ord('A') + i)
        for i in range(26, 52):
            Base64.look_up_base64_alphabet[i] = chr(ord('a') + (i - 26))
        for i in range(52, 62):
            Base64.look_up_base64_alphabet[i] = chr(ord('0') + (i - 52))
        Base64.look_up_base64_alphabet[62] = '+'
        Base64.look_up_base64_alphabet[63] = '/'

    @staticmethod
    def is_white_space(octect):
        """
        判断字符是否为空白字符（空格、回车、换行、制表符等）
        """
        return octect in (0x20, 0xd, 0xa, 0x9)

    @staticmethod
    def is_pad(octect):
        """
        判断字符是否为Base64编码中的填充字符（'='）
        """
        return octect == Base64.PAD

    @staticmethod
    def is_data(octect):
        """
        判断字符是否为Base64编码中的有效数据字符
        """
        return ord(octect) < Base64.BASELENGTH and Base64.base64_alphabet[ord(octect)]!= -1

    @staticmethod
    def is_valid_base64(encoded):
        """
        验证输入的是否是合法的Base64编码字符串
        """
        if encoded is None:
            return False
        base64_data = list(encoded)
        # 去除空白字符
        len_data = Base64._remove_white_space(base64_data)
        if len_data % Base64.FOURBYTE!= 0:
            return False
        for char in base64_data:
            if not Base64.is_data(char):
                return False
        return True

    @staticmethod
    def encode(binary_data):
        """
        将字节数据进行Base64编码
        """
        if binary_data is None:
            return None
        length_data_bits = len(binary_data) * Base64.EIGHTBIT
        if length_data_bits == 0:
            return ""
        fewer_than_24bits = length_data_bits % Base64.TWENTYFOURBITGROUP
        number_triplets = length_data_bits // Base64.TWENTYFOURBITGROUP
        number_quartet = number_triplets + 1 if fewer_than_24bits!= 0 else number_triplets
        encoded_data = [""] * (number_quartet * 4)

        k = l = b1 = b2 = b3 = 0
        encoded_index = data_index = 0
        for i in range(number_triplets):
            b1 = binary_data[data_index]
            b2 = binary_data[data_index + 1]
            b3 = binary_data[data_index + 2]
            data_index += 3

            l = b2 & 0x0f
            k = b1 & 0x03

            val1 = (b1 >> 2) if (b1 & Base64.SIGN) == 0 else (b1 >> 2) ^ 0xc0
            val2 = (b2 >> 4) if (b2 & Base64.SIGN) == 0 else (b2 >> 4) ^ 0xf0
            val3 = (b3 >> 6) if (b3 & Base64.SIGN) == 0 else (b3 >> 6) ^ 0xfc

            encoded_data[encoded_index] = Base64.look_up_base64_alphabet[val1]
            encoded_index += 1
            encoded_data[encoded_index] = Base64.look_up_base64_alphabet[val2 | (k << 4)]
            encoded_index += 1
            encoded_data[encoded_index] = Base64.look_up_base64_alphabet[(l << 2) | val3]
            encoded_index += 1
            encoded_data[encoded_index] = Base64.look_up_base64_alphabet[b3 & 0x3f]
            encoded_index += 1

        if fewer_than_24bits == Base64.EIGHTBIT:
            b1 = binary_data[data_index]
            k = b1 & 0x03
            val1 = (b1 >> 2) if (b1 & Base64.SIGN) == 0 else (b1 >> 2) ^ 0xc0
            encoded_data[encoded_index] = Base64.look_up_base64_alphabet[val1]
            encoded_index += 1
            encoded_data[encoded_index] = Base64.look_up_base64_alphabet[k << 4]
            encoded_index += 1
            encoded_data[encoded_index] = Base64.PAD
            encoded_index += 1
            encoded_data[encoded_index] = Base64.PAD
            encoded_index += 1
        elif fewer_than_24bits == Base64.SIXTEENBIT:
            b1 = binary_data[data_index]
            b2 = binary_data[data_index + 1]
            l = b2 & 0x0f
            k = b1 & 0x03

            val1 = (b1 >> 2) if (b1 & Base64.SIGN) == 0 else (b1 >> 2) ^ 0xc0
            val2 = (b2 >> 4) if (b2 & Base64.SIGN) == 0 else (b2 >> 4) ^ 0xf0

            encoded_data[encoded_index] = Base64.look_up_base64_alphabet[val1]
            encoded_index += 1
            encoded_data[encoded_index] = Base64.look_up_base64_alphabet[val2 | (k << 4)]
            encoded_index += 1
            encoded_data[encoded_index] = Base64.look_up_base64_alphabet[l << 2]
            encoded_index += 1
            encoded_data[encoded_index] = Base64.PAD
            encoded_index += 1
        return "".join(encoded_data)

    @staticmethod
    def decode(encoded):
        """
        将Base64编码的字符串解码为字节数据
        """
        if not Base64.is_valid_base64(encoded):
            return None
        base64_data = list(encoded)
        # 去除空白字符
        len_data = Base64._remove_white_space(base64_data)
        if len_data % Base64.FOURBYTE!= 0:
            return None
        number_quadruple = len_data // Base64.FOURBYTE
        if number_quadruple == 0:
            return bytes()

        decoded_data = bytearray()
        b1 = b2 = b3 = b4 = d1 = d2 = d3 = d4 = 0
        i = encoded_index = data_index = 0
        decoded_data = bytearray(number_quadruple * 3)
        for _ in range(number_quadruple - 1):
            d1 = base64_data[data_index]
            d2 = base64_data[data_index + 1]
            d3 = base64_data[data_index + 2]
            d4 = base64_data[data_index + 3]
            data_index += 4

            if not Base64.is_data(d1) or not Base64.is_data(d2) or not Base64.is_data(d3) or not Base64.is_data(d4):
                return None
            b1 = Base64.base64_alphabet[ord(d1)]
            b2 = Base64.base64_alphabet[ord(d2)]
            b3 = Base64.base64_alphabet[ord(d3)]
            b4 = Base64.base64_alphabet[ord(d4)]

            result = (b1 << 2 | b2 >> 4)
            if result > 255:
                result %= 256
            decoded_data[encoded_index] = result.to_bytes(1, 'big')[0]
            encoded_index += 1

            result = ((b2 & 0xf) << 4 | (b3 >> 2) & 0xf)
            if result > 255:
                result %= 256
            decoded_data[encoded_index] = result.to_bytes(1, 'big')[0]
            encoded_index += 1

            result = (b3 << 6 | b4)
            if result > 255:
                result %= 256
            decoded_data[encoded_index] = result.to_bytes(1, 'big')[0]
            encoded_index += 1
        d1 = base64_data[data_index]
        d2 = base64_data[data_index + 1]
        if not Base64.is_data(d1) or not Base64.is_data(d2):
            return None
        b1 = Base64.base64_alphabet[ord(d1)]
        b2 = Base64.base64_alphabet[ord(d2)]

        d3 = base64_data[data_index + 2]
        d4 = base64_data[data_index + 3]
        if not Base64.is_data(d3) or not Base64.is_data(d4):
            if Base64.is_pad(d3) and Base64.is_pad(d4):
                if (b2 & 0xf)!= 0:
                    return None
                tmp = bytearray(i * 3 + 1)
                tmp[:i * 3] = decoded_data[:i * 3]
                result = (b1 << 2 | b2 >> 4)
                if result > 255:
                    result %= 256
                tmp[encoded_index] = result.to_bytes(1, 'big')[0]
                return bytes(tmp)
            elif not Base64.is_pad(d3) and Base64.is_pad(d4):
                b3 = Base64.base64_alphabet[ord(d3)]
                result = (b1 << 2 | b2 >> 4)
                if result > 255:
                    result %= 256
                tmp = bytearray(i * 3 + 2)
                tmp[:i * 3] = decoded_data[:i * 3]
                tmp[encoded_index] = result.to_bytes(1, 'big')[0]
                result = ((b2 & 0xf) << 4 | (b3 >> 2) & 0xf)
                if result > 255:
                    result %= 256
                tmp[encoded_index + 1] = result.to_bytes(1, 'big')[0]
                return bytes(tmp)
            else:
                return None
        else:
            b3 = Base64.base64_alphabet[ord(d3)]
            b4 = Base64.base64_alphabet[ord(d4)]

            result = (b1 << 2 | b2 >> 4)
            if result > 255:
                result %= 256
            decoded_data[encoded_index] = result.to_bytes(1, 'big')[0]
            encoded_index += 1

            result = ((b2 & 0xf) << 4 | (b3 >> 2) & 0xf)
            if result > 255:
                result %= 256
            decoded_data[encoded_index] = result.to_bytes(1, 'big')[0]
            encoded_index += 1

            result = (b3 << 6 | b4)
            if result > 255:
                result %= 256
            decoded_data[encoded_index] = result.to_bytes(1, 'big')[0]
            encoded_index += 1
        return bytes(decoded_data)

    @staticmethod
    def _remove_white_space(data):
        """
        去除Base64编码数据中的空白字符，返回去除后的有效字符长度
        """
        if data is None:
            return 0
        new_size = 0
        for char in data:
            if not Base64.is_white_space(char):
                data[new_size] = char
                new_size += 1
        return new_size

if __name__ == '__main__':
    # 初始化Base64编码字符映射表（模拟Java中的静态初始化块执行）
    Base64._init_alphabet()

    # 测试编码
    original_data = b"Hello, World!"
    encoded_result = Base64.encode(original_data)
    print(encoded_result)

    # 测试解码
    decoded_result = Base64.decode(encoded_result)
    print(decoded_result)