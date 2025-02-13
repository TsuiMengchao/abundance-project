import decimal
import re


class Convert:
    """
    类型转换器，对应Java版本中的Convert类
    """

    @staticmethod
    def to_str(value, default_value=None):
        """
        转换为字符串，如果给定的值为None，或者转换失败，返回默认值，转换失败不会报错
        """
        if value is None:
            return default_value
        return str(value) if isinstance(value, str) else str(value)

    @staticmethod
    def to_str_simple(value):
        """
        转换为字符串，如果给定的值为None，或者转换失败，返回默认值None，转换失败不会报错
        """
        return Convert.to_str(value, None)

    @staticmethod
    def to_char(value, default_value=None):
        """
        转换为字符，如果给定的值为None，或者转换失败，返回默认值，转换失败不会报错
        """
        if value is None:
            return default_value
        if isinstance(value, str) and len(value) == 1:
            return value
        value_str = Convert.to_str(value)
        return value_str[0] if value_str else default_value

    @staticmethod
    def to_char_simple(value):
        """
        转换为字符，如果给定的值为None，或者转换失败，返回默认值None，转换失败不会报错
        """
        return Convert.to_char(value, None)

    @staticmethod
    def to_byte(value, default_value=None):
        """
        转换为byte，如果给定的值为None，或者转换失败，返回默认值，转换失败不会报错
        """
        if value is None:
            return default_value
        if isinstance(value, bytes):
            return value[0] if value else default_value
        if isinstance(value, int):
            return value.to_bytes(1, 'big')
        value_str = Convert.to_str(value)
        if not value_str:
            return default_value
        try:
            return int(value_str).to_bytes(1, 'big')
        except ValueError:
            return default_value

    @staticmethod
    def to_byte_simple(value):
        """
        转换为byte，如果给定的值为None，或者转换失败，返回默认值None，转换失败不会报错
        """
        return Convert.to_byte(value, None)

    @staticmethod
    def to_short(value, default_value=None):
        """
        转换为Short，如果给定的值为None，或者转换失败，返回默认值，转换失败不会报错
        """
        if value is None:
            return default_value
        if isinstance(value, int) and -32768 <= value <= 32767:
            return value
        value_str = Convert.to_str(value).strip()
        if not value_str:
            return default_value
        try:
            return int(value_str)
        except ValueError:
            return default_value

    @staticmethod
    def to_short_simple(value):
        """
        转换为Short，如果给定的值为None，或者转换失败，返回默认值None，转换失败不会报错
        """
        return Convert.to_short(value, None)

    @staticmethod
    def to_number(value, default_value=None):
        """
        转换为Number，如果给定的值为None，或者转换失败，返回默认值，转换失败不会报错
        """
        if value is None:
            return default_value
        if isinstance(value, (int, float, decimal.Decimal)):
            return value
        value_str = Convert.to_str(value)
        if not value_str:
            return default_value
        try:
            return decimal.Decimal(value_str)
        except decimal.InvalidOperation:
            return default_value

    @staticmethod
    def to_number_simple(value):
        """
        转换为Number，如果给定的值为None，或者转换失败，返回默认值None，转换失败不会报错
        """
        return Convert.to_number(value, None)

    @staticmethod
    def to_int(value, default_value=None):
        """
        转换为int，如果给定的值为None，或者转换失败，返回默认值，转换失败不会报错
        """
        if value is None:
            return default_value
        if isinstance(value, int):
            return value
        value_str = Convert.to_str(value).strip()
        if not value_str:
            return default_value
        try:
            return int(value_str)
        except ValueError:
            return default_value

    @staticmethod
    def to_int_simple(value):
        """
        转换为int，如果给定的值为None，或者转换失败，返回默认值None，转换失败不会报错
        """
        return Convert.to_int(value, None)

    @staticmethod
    def to_int_array(str_value, split=","):
        """
        转换为Integer数组
        """
        if not str_value:
            return []
        arr = str_value.split(split)
        return [Convert.to_int(v) for v in arr]

    @staticmethod
    def to_long_array(str_value, split=","):
        """
        转换为Long数组
        """
        if not str_value:
            return []
        arr = str_value.split(split)
        return [Convert.to_long(v) for v in arr]

    @staticmethod
    def to_str_array(str_value, split=","):
        """
        转换为String数组
        """
        if not str_value:
            return []
        return str_value.split(split)

    @staticmethod
    def to_long(value, default_value=None):
        """
        转换为long，如果给定的值为None，或者转换失败，返回默认值，转换失败不会报错
        """
        if value is None:
            return default_value
        if isinstance(value, int):
            return value
        value_str = Convert.to_str(value).strip()
        if not value_str:
            return default_value
        try:
            return int(value_str)
        except ValueError:
            return default_value

    @staticmethod
    def to_long_simple(value):
        """
        转换为long，如果给定的值为None，或者转换失败，返回默认值None，转换失败不会报错
        """
        return Convert.to_long(value, None)

    @staticmethod
    def to_double(value, default_value=None):
        """
        转换为double，如果给定的值为None，或者转换失败，返回默认值，转换失败不会报错
        """
        if value is None:
            return default_value
        if isinstance(value, float):
            return value
        value_str = Convert.to_str(value).strip()
        if not value_str:
            return default_value
        try:
            return float(value_str)
        except ValueError:
            return default_value

    @staticmethod
    def to_double_simple(value):
        """
        转换为double，如果给定的值为None，或者转换失败，返回默认值None，转换失败不会报错
        """
        return Convert.to_double(value, None)

    @staticmethod
    def to_float(value, default_value=None):
        """
        转换为Float，如果给定的值为None，或者转换失败，返回默认值，转换失败不会报错
        """
        if value is None:
            return default_value
        if isinstance(value, float):
            return value
        value_str = Convert.to_str(value).strip()
        if not value_str:
            return default_value
        try:
            return float(value_str)
        except ValueError:
            return default_value

    @staticmethod
    def to_float_simple(value):
        """
        转换为Float，如果给定的值为None，或者转换失败，返回默认值None，转换失败不会报错
        """
        return Convert.to_float(value, None)

    @staticmethod
    def to_bool(value, default_value=None):
        """
        转换为boolean，String支持的值为：true、false、yes、ok、no，1,0 如果给定的值为None，或者转换失败，返回默认值，转换失败不会报错
        """
        if value is None:
            return default_value
        if isinstance(value, bool):
            return value
        value_str = Convert.to_str(value).lower().strip()
        if value_str in ["true", "yes", "ok", "1"]:
            return True
        elif value_str in ["false", "no", "0"]:
            return False
        return default_value

    @staticmethod
    def to_bool_simple(value):
        """
        转换为boolean，如果给定的值为None，或者转换失败，返回默认值None，转换失败不会报错
        """
        return Convert.to_bool(value, None)

    @staticmethod
    def to_enum(clazz, value, default_value=None):
        """
        转换为Enum对象，如果给定的值为None，或者转换失败，返回默认值
        """
        if value is None:
            return default_value
        if isinstance(value, clazz):
            return value
        value_str = Convert.to_str(value)
        if not value_str:
            return default_value
        try:
            return clazz(value_str)
        except ValueError:
            return default_value

    @staticmethod
    def to_enum_simple(clazz, value):
        """
        转换为Enum对象，如果给定的值为None，或者转换失败，返回默认值None
        """
        return Convert.to_enum(clazz, value, None)

    @staticmethod
    def to_big_integer(value, default_value=None):
        """
        转换为BigInteger，如果给定的值为None，或者转换失败，返回默认值，转换失败不会报错
        """
        if value is None:
            return default_value
        if isinstance(value, int):
            return decimal.Decimal(value).to_integral_value()
        value_str = Convert.to_str(value)
        if not value_str:
            return default_value
        try:
            return decimal.Decimal(value_str).to_integral_value()
        except decimal.InvalidOperation:
            return default_value

    @staticmethod
    def to_big_integer_simple(value):
        """
        转换为BigInteger，如果给定的值为None，或者转换失败，返回默认值None，转换失败不会报错
        """
        return Convert.to_big_integer(value, None)

    @staticmethod
    def to_big_decimal(value, default_value=None):
        """
        转换为BigDecimal，如果给定的值为None，或者转换失败，返回默认值，转换失败不会报错
        """
        if value is None:
            return default_value
        if isinstance(value, (int, float)):
            return decimal.Decimal(value)
        value_str = Convert.to_str(value)
        if not value_str:
            return default_value
        try:
            return decimal.Decimal(value_str)
        except decimal.InvalidOperation:
            return default_value

    @staticmethod
    def to_big_decimal_simple(value):
        """
        转换为BigDecimal，如果给定的值为None，或者转换失败，返回默认值None，转换失败不会报错
        """
        return Convert.to_big_decimal(value, None)

    @staticmethod
    def utf8_str(obj):
        """
        将对象转为字符串（使用UTF-8字符集）
        """
        return Convert.str(obj, 'utf-8')

    @staticmethod
    def str(obj, charset_name='utf-8'):
        """
        将对象转为字符串，支持多种类型的转换逻辑
        """
        if obj is None:
            return None
        if isinstance(obj, str):
            return obj
        elif isinstance(obj, (bytes, bytearray)):
            return obj.decode(charset_name, 'replace')
        elif isinstance(obj, list):
            return str(obj)
        return str(obj)

    @staticmethod
    def to_sbc(input, not_convert_set=None):
        """
        半角转全角
        """
        if not input:
            return input
        result = ""
        for char in input:
            if not_convert_set and char in not_convert_set:
                result += char
                continue
            if char == " ":
                result += "\u3000"
            elif ord(char) < 127:
                result += chr(ord(char) + 65248)
            else:
                result += char
        return result

    @staticmethod
    def to_dbc(input, not_convert_set=None):
        """
        全角转半角
        """
        if not input:
            return input
        result = ""
        for char in input:
            if not_convert_set and char in not_convert_set:
                result += char
                continue
            if char == "\u3000":
                result += " "
            elif 65281 <= ord(char) <= 65374:
                result += chr(ord(char) - 65248)
            else:
                result += char
        return result

    @staticmethod
    def digit_uppercase(n):
        """
        数字金额大写转换
        """
        fraction = ["角", "分"]
        digit = ["零", "壹", "贰", "叁", "肆", "伍", "陆", "柒", "捌", "玖"]
        unit = [["元", "万", "亿"], ["", "拾", "佰", "仟"]]

        head = "负" if n < 0 else ""
        n = abs(n)

        s = ""
        for i in range(len(fraction)):
            d = int((n * 10 ** (i + 1)) % 10)
            s += (digit[d] + fraction[i]).replace("零.", "")

        if s == "":
            s = "整"

        integer_part = int(n)
        result = ""
        for i in range(len(unit[0])):
            part = ""
            temp = integer_part
            for j in range(len(unit[1])):
                part = digit[temp % 10] + unit[1][j] + part
                temp //= 10
            result = part.replace("(零.)*零$", "").replace("^$", "零") + unit[0][i] + result
            integer_part //= 10000 if i < 2 else 100000000

        return head + result.replace("(零.)*零元", "元").replace("(零.)+", "零").replace("^整$", "零元整")


if __name__ == "__main__":
    # 示例使用
    print(Convert.to_str(123))
    print(Convert.to_char("a"))
    print(Convert.to_byte(10))
    print(Convert.to_short(100))
    print(Convert.to_number(12.34))
    print(Convert.to_int(100))
    print(Convert.to_int_array("1,2,3"))
    print(Convert.to_long(1000))
    print(Convert.to_double(12.34))
    print(Convert.to_float(12.34))
    print(Convert.to_bool("true"))
    print(Convert.to_enum(int, 1))
    print(Convert.to_big_integer(100))
    print(Convert.to_big_decimal(12.34))
    print(Convert.utf8_str("测试字符串"))
    print(Convert.to_sbc("abc 123"))
    print(Convert.to_dbc("ＡＢＣ　１２３"))
    print(Convert.digit_uppercase(123.45))