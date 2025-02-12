import pandas as pd
import psutil


# from ip2region import Ip2Region

class StringUtils:
    SEPARATOR = '_'
    UNKNOWN = "unknown"
    NULLSTR = ""
    SEPARATOR = '_'
    ASTERISK = '*'

    @staticmethod
    def to_camel_case(s):
        """
        驼峰命名法工具，将下划线分隔的字符串转换为驼峰命名形式（首字母小写）
        例如："hello_world" -> "helloWorld"
        """
        if s is None:
            return None
        s = s.lower()
        result = ""
        upper_case = False
        for index, char in enumerate(s):
            if char == StringUtils.SEPARATOR:
                upper_case = True
            else:
                if upper_case:
                    result += char.upper()
                    upper_case = False
                else:
                    result += char
        return result

    @staticmethod
    def to_capitalize_camel_case(s):
        """
        驼峰命名法工具，将字符串转换为驼峰命名形式（首字母大写）
        例如："hello_world" -> "HelloWorld"
        """
        if s is None:
            return None
        s = StringUtils.to_camel_case(s)
        return s[0].upper() + s[1:]

    @staticmethod
    def to_under_score_case(s):
        """
        驼峰命名法工具，将驼峰命名的字符串转换为下划线分隔形式
        例如："helloWorld" -> "hello_world"
        """
        if s is None:
            return None
        result = ""
        upper_case = False
        for index, char in enumerate(s):
            next_upper_case = index < len(s) - 1 and char.isupper() and s[index + 1].isupper()
            if index > 0 and char.isupper():
                if not upper_case or not next_upper_case:
                    result += StringUtils.SEPARATOR
                upper_case = True
            else:
                upper_case = False
            result += char.lower()
        return result

    @staticmethod
    def get_city_info(ip):
        # 初始化Ip2Region对象，指定数据库文件路径
        searcher = Ip2Region('ip2region.db')
        try:
            # 执行查询
            data = searcher.memorySearch(ip)
            if data:
                # 解析结果，提取城市信息
                city_info = data.region.split('|')[2]
                return city_info
            else:
                return "未找到对应城市信息"
        except Exception as e:
            print(f"查询出错: {e}")
            return None
        finally:
            # 关闭资源
            searcher.close()

    @staticmethod
    def get_week_day():
        """
        获得当天是周几
        """
        week_days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
        today = pd.Timestamp.now()
        return week_days[today.dayofweek]

    @staticmethod
    def get_local_ip():
        """
        获取当前机器的IP，遍历网络接口查找合适的IP地址
        """
        addrs = psutil.net_if_addrs()
        for interface, addr_list in addrs.items():
            for addr in addr_list:
                if addr.family == 2:  # AF_INET表示IPv4地址
                    ip = addr.address
                    if not ip.startswith("127."):
                        return ip
        return ""

    @staticmethod
    def nvl(value, defaultValue):
        """
        获取参数不为空值，对应Java版本中的nvl方法
        """
        return value if value is not None else defaultValue

    @staticmethod
    def isEmpty(collection):
        """
        判断一个Collection是否为空， 包含List，Set，Queue，对应Java版本中的isEmpty方法（针对可迭代对象）
        """
        return collection is None or len(collection) == 0

    @staticmethod
    def isNotEmpty(collection):
        """
        判断一个Collection是否非空，包含List，Set，Queue，对应Java版本中的isNotEmpty方法（针对可迭代对象）
        """
        return not StringUtils.isEmpty(collection)

    @staticmethod
    def isEmptyArray(objects):
        """
        判断一个对象数组是否为空，对应Java版本中的isEmpty方法（针对对象数组）
        """
        return objects is None or len(objects) == 0

    @staticmethod
    def isNotEmptyArray(objects):
        """
        判断一个对象数组是否非空，对应Java版本中的isNotEmpty方法（针对对象数组）
        """
        return not StringUtils.isEmptyArray(objects)

    @staticmethod
    def isEmptyMap(mapData):
        """
        判断一个Map是否为空，对应Java版本中的isEmpty方法（针对字典类型）
        """
        return mapData is None or len(mapData) == 0

    @staticmethod
    def isNotEmptyMap(mapData):
        """
        判断一个Map是否非空，对应Java版本中的isNotEmpty方法（针对字典类型）
        """
        return not StringUtils.isEmptyMap(mapData)

    @staticmethod
    def isEmptyStr(string):
        """
        判断一个字符串是否为空串，对应Java版本中的isEmpty方法（针对字符串）
        """
        return string is None or string.strip() == ""

    @staticmethod
    def isNotEmptyStr(string):
        """
        判断一个字符串是否为非空串，对应Java版本中的isNotEmpty方法（针对字符串）
        """
        return not StringUtils.isEmptyStr(string)

    @staticmethod
    def isNull(object):
        """
        判断一个对象是否为空，对应Java版本中的isNull方法
        """
        return object is None

    @staticmethod
    def isNotNull(object):
        """
        判断一个对象是否非空，对应Java版本中的isNotNull方法
        """
        return not StringUtils.isNull(object)

    @staticmethod
    def isArray(object):
        """
        判断一个对象是否是数组类型（Python中可检查是否为可迭代对象等类似概念），对应Java版本中的isArray方法
        """
        return hasattr(object, '__iter__') and not isinstance(object, str)

    @staticmethod
    def trim(string):
        """
        去空格，对应Java版本中的trim方法
        """
        return string.strip() if string else ""

    @staticmethod
    def hide(string, startInclude, endExclude):
        """
        替换指定字符串的指定区间内字符为"*"，对应Java版本中的hide方法
        """
        if StringUtils.isEmptyStr(string):
            return ""
        stringLength = len(string)
        if startInclude > stringLength:
            return ""
        if endExclude > stringLength:
            endExclude = stringLength
        if startInclude > endExclude:
            return ""
        charList = list(string)
        for i in range(stringLength):
            if startInclude <= i < endExclude:
                charList[i] = '*'
        return "".join(charList)

    @staticmethod
    def substring(string, start):
        """
        截取字符串，对应Java版本中的substring方法（单参数版本）
        """
        if string is None:
            return ""
        if start < 0:
            start = len(string) + start
        if start < 0:
            start = 0
        if start > len(string):
            return ""
        return string[start:]

    @staticmethod
    def substringFull(string, start, end):
        """
        截取字符串，对应Java版本中的substring方法（双参数版本）
        """
        if string is None:
            return ""
        if end < 0:
            end = len(string) + end
        if start < 0:
            start = len(string) + start
        if end > len(string):
            end = len(string)
        if start > end:
            return ""
        if start < 0:
            start = 0
        if end < 0:
            end = 0
        return string[start:end]

    @staticmethod
    def hasText(string):
        """
        判断是否为空，并且不是空白字符，对应Java版本中的hasText方法
        """
        return string is not None and string.strip()!= "" and any(not char.isspace() for char in string)

    @staticmethod
    def format(template, *params):
        """
        格式化文本，对应Java版本中的format方法
        """
        if not params or not template:
            return template
        # 这里简单模拟占位符替换，实际可能需要更复杂的处理逻辑，比如转义等情况
        result = template
        for index, param in enumerate(params):
            result = result.replace("{}", str(param), 1)
        return result

    @staticmethod
    def isHttp(link):
        """
        是否为http(s)://开头，对应Java版本中的ishttp方法
        """
        return link.startswith(("http://", "https://"))

    @staticmethod
    def containsAny(collection, *array):
        """
        判断给定的collection列表中是否包含数组array，判断给定的数组array中是否包含给定的元素value，对应Java版本中的containsAny方法
        """
        if StringUtils.isEmpty(collection) or StringUtils.isEmptyArray(array):
            return False
        for element in array:
            if element in collection:
                return True
        return False

    @staticmethod
    def toUnderScoreCase(string):
        """
        驼峰转下划线命名，对应Java版本中的toUnderScoreCase方法
        """
        if string is None:
            return None
        result = ""
        for index in range(len(string)):
            char = string[index]
            if index > 0:
                prevChar = string[index - 1]
                isPrevCharUpperCase = prevChar.isupper()
            else:
                isPrevCharUpperCase = False
            isCharUpperCase = char.isupper()
            if index < len(string) - 1:
                nextChar = string[index + 1]
                isNextCharUpperCase = nextChar.isupper()
            else:
                isNextCharUpperCase = False
            if (isPrevCharUpperCase and isCharUpperCase and not isNextCharUpperCase) or (
                    index!= 0 and not isPrevCharUpperCase and isCharUpperCase):
                result += "_"
            result += char.lower()
        return result

    @staticmethod
    def inStringIgnoreCase(string, *strs):
        """
        是否包含字符串，对应Java版本中的inStringIgnoreCase方法
        """
        if string is not None and strs is not None:
            for s in strs:
                if string.lower() == s.lower().strip():
                    return True
        return False

    @staticmethod
    def convertToCamelCase(name):
        """
        将下划线大写方式命名的字符串转换为驼峰式，对应Java版本中的convertToCamelCase方法
        """
        if not name or name == "":
            return ""
        if "_" not in name:
            return name[0].upper() + name[1:].lower()
        parts = name.split("_")
        result = ""
        for part in parts:
            if part:
                result += part[0].upper() + part[1:].lower()
        return result

    @staticmethod
    def toCamelCase(s):
        """
        驼峰式命名法，例如：user_name->userName，对应Java版本中的toCamelCase方法
        """
        if s is None:
            return None
        if s.find("_") == -1:
            return s
        s = s.lower()
        result = ""
        upperCase = False
        for char in s:
            if char == "_":
                upperCase = True
            elif upperCase:
                result += char.upper()
                upperCase = False
            else:
                result += char
        return result

    @staticmethod
    def matches(string, strs):
        """
        查找指定字符串是否匹配指定字符串列表中的任意一个字符串，对应Java版本中的matches方法
        """
        if StringUtils.isEmptyStr(string) or not strs:
            return False
        for pattern in strs:
            if StringUtils.isMatch(pattern, string):
                return True
        return False

    @staticmethod
    def isMatch(pattern, url):
        """
        判断url是否与规则配置，对应Java版本中的isMatch方法
        """
        try:
            from urllib.parse import urlparse
            import fnmatch

            # 提取路径部分（去除协议、域名等）
            path = urlparse(url).path
            return fnmatch.fnmatch(path, pattern)
        except ImportError:
            print("缺少必要的库，无法进行匹配判断，请确保已安装urllib.parse和fnmatch库")
            return False

    @staticmethod
    def cast(obj):
        """
        类型转换（简单模拟，实际使用需谨慎，可能需要更多类型检查等），对应Java版本中的cast方法
        """
        return obj

    @staticmethod
    def padl(s, size, c='0'):
        """
        字符串左补齐。如果原始字符串s长度大于size，则只保留最后size个字符，对应Java版本中的padl方法（针对字符串）
        """
        s = str(s)
        if s is None:
            return c * size
        sLength = len(s)
        if sLength <= size:
            return (c * (size - sLength)) + s
        return s[-size:]

if __name__ == "__main__":
    # 测试to_camel_case方法
    camel_case_result = StringUtils.to_camel_case("hello_world")
    print(f"to_camel_case result: {camel_case_result}")

    # 测试to_capitalize_camel_case方法
    capitalize_camel_case_result = StringUtils.to_capitalize_camel_case("hello_world")
    print(f"to_capitalize_camel_case result: {capitalize_camel_case_result}")

    # 测试to_under_score_case方法
    under_score_case_result = StringUtils.to_under_score_case("helloWorld")
    print(f"to_under_score_case result: {under_score_case_result}")

    # 模拟请求头信息（仅为测试get_ip和get_browser方法简单构造）
    mock_request_headers = {
        "x-forwarded-for": "192.168.1.100",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    mock_request = type('MockRequest', (), {'headers': mock_request_headers, 'remote_addr': '127.0.0.1'})()

    # # 测试get_ip方法
    # ip_result = StringUtils.get_ip(mock_request)
    # print(f"get_ip result: {ip_result}")

    # # 测试get_city_info方法
    # city_info_result = StringUtils.get_city_info(ip_result)
    # print(f"get_city_info result: {city_info_result}")

    # 测试get_week_day方法
    week_day_result = StringUtils.get_week_day()
    print(f"get_week_day result: {week_day_result}")

    # 测试get_local_ip方法
    local_ip_result = StringUtils.get_local_ip()
    print(f"get_local_ip result: {local_ip_result}")

    # 测试nvl方法
    result_nvl = StringUtils.nvl(None, "default_value")
    print(f"nvl方法测试结果: {result_nvl}")

    # 测试isEmpty方法（针对可迭代对象）
    test_list = []
    result_isEmpty_list = StringUtils.isEmpty(test_list)
    print(f"isEmpty方法（针对列表）测试结果: {result_isEmpty_list}")

    # 测试isNotEmpty方法（针对可迭代对象）
    result_isNotEmpty_list = StringUtils.isNotEmpty(test_list)
    print(f"isNotEmpty方法（针对列表）测试结果: {result_isNotEmpty_list}")

    # 测试isEmptyStr方法
    test_str = ""
    result_isEmptyStr = StringUtils.isEmptyStr(test_str)
    print(f"isEmptyStr方法测试结果: {result_isEmptyStr}")

    # 测试isNotEmptyStr方法
    test_str = "not empty"
    result_isNotEmptyStr = StringUtils.isNotEmptyStr(test_str)
    print(f"isNotEmptyStr方法测试结果: {result_isNotEmptyStr}")

    # 测试trim方法
    test_str_with_space = "   hello   "
    result_trim = StringUtils.trim(test_str_with_space)
    print(f"trim方法测试结果: {result_trim}")

    # 测试hide方法
    test_hide_str = "abcdefg"
    result_hide = StringUtils.hide(test_hide_str, 2, 5)
    print(f"hide方法测试结果: {result_hide}")

    # 测试substring方法（单参数版本）
    test_substring_str = "hello world"
    result_substring = StringUtils.substring(test_substring_str, 6)
    print(f"substring方法（单参数版本）测试结果: {result_substring}")

    # 测试substringFull方法（双参数版本）
    result_substringFull = StringUtils.substringFull(test_substring_str, 6, 11)
    print(f"substringFull方法（双参数版本）测试结果: {result_substringFull}")

    # 测试hasText方法
    test_hasText_str = "   "
    result_hasText = StringUtils.hasText(test_hasText_str)
    print(f"hasText方法测试结果: {result_hasText}")

    # 测试format方法
    test_format_template = "This is {} for {}"
    test_format_params = ["a", "b"]
    result_format = StringUtils.format(test_format_template, *test_format_params)
    print(f"format方法测试结果: {result_format}")

    # 测试isHttp方法
    test_http_link = "https://www.example.com"
    result_isHttp = StringUtils.isHttp(test_http_link)
    print(f"isHttp方法测试结果: {result_isHttp}")

    # 测试containsAny方法
    test_collection = ["a", "b", "c"]
    test_array = ["b", "d"]
    result_containsAny = StringUtils.containsAny(test_collection, *test_array)
    print(f"containsAny方法测试结果: {result_containsAny}")

    # 测试toUnderScoreCase方法
    test_toUnderScoreCase_str = "helloWorld"
    result_toUnderScoreCase = StringUtils.toUnderScoreCase(test_toUnderScoreCase_str)
    print(f"toUnderScoreCase方法测试结果: {result_toUnderScoreCase}")

    # 测试inStringIgnoreCase方法
    test_inStringIgnoreCase_str = "Hello"
    test_inStringIgnoreCase_strs = ["hello", "world"]
    result_inStringIgnoreCase = StringUtils.inStringIgnoreCase(test_inStringIgnoreCase_str, *test_inStringIgnoreCase_strs)
    print(f"inStringIgnoreCase方法测试结果: {result_inStringIgnoreCase}")

    # 测试convertToCamelCase方法
    test_convertToCamelCase_str = "HELLO_WORLD"
    result_convertToCamelCase = StringUtils.convertToCamelCase(test_convertToCamelCase_str)
    print(f"convertToCamelCase方法测试结果: {result_convertToCamelCase}")

    # 测试toCamelCase方法
    test_toCamelCase_str = "user_name"
    result_toCamelCase = StringUtils.toCamelCase(test_toCamelCase_str)
    print(f"toCamelCase方法测试结果: {result_toCamelCase}")

    # 测试matches方法
    test_matches_str = "test"
    test_matches_strs = ["test", "other"]
    result_matches = StringUtils.matches(test_matches_str, test_matches_strs)
    print(f"matches方法测试结果: {result_matches}")

    # 测试isMatch方法
    test_isMatch_pattern = "test/*"
    test_isMatch_url = "test/file.txt"
    result_isMatch = StringUtils.isMatch(test_isMatch_pattern, test_isMatch_url)
    print(f"isMatch方法测试结果: {result_isMatch}")

    # 测试cast方法
    test_cast_obj = 123
    result_cast = StringUtils.cast(test_cast_obj)
    print(f"cast方法测试结果: {result_cast}")

    # 测试padl方法（针对数字）
    test_padl_num = 12
    result_padl = StringUtils.padl(test_padl_num, 5)
    print(f"padl方法（针对数字）测试结果: {result_padl}")

    # 测试padlFull方法（针对字符串）
    test_padlFull_str = "abc"
    result_padlFull = StringUtils.padl(test_padlFull_str, 5, '*')
    print(f"padl方法（针对字符串）测试结果: {result_padlFull}")