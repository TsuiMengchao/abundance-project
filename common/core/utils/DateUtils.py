from datetime import datetime, date, timedelta, timezone
import time


class DateUtils:
    YYYY = "yyyy"
    YYYY_MM = "yyyy-MM"
    YYYY_MM_DD = "yyyy-MM-dd"
    YYYYMMDDHHMMSS = "yyyyMMddHHmmss"
    YYYY_MM_DD_HH_MM_SS = "yyyy-MM-dd HH:mm:ss"
    parse_patterns = [
        "yyyy-MM-dd", "yyyy-MM-dd HH:mm:ss", "yyyy-MM-dd HH:mm", "yyyy-MM",
        "yyyy/MM/dd", "yyyy/MM/dd HH:mm:ss", "yyyy/MM/dd HH:mm", "yyyy/MM",
        "yyyy.MM.dd", "yyyy.MM.dd HH:mm:ss", "yyyy.MM.dd HH:mm", "yyyy.MM"
    ]

    @staticmethod
    def getNowDate():
        """
        获取当前Date型日期，对应Java版本中的getNowDate方法
        """
        return datetime.now()

    @staticmethod
    def getDate():
        """
        获取当前日期，默认格式为yyyy-MM-dd，对应Java版本中的getDate方法
        """
        return DateUtils.dateTimeNow(DateUtils.YYYY_MM_DD)

    @staticmethod
    def getTime():
        """
        获取当前时间，格式为yyyy-MM-dd HH:mm:ss，对应Java版本中的getTime方法
        """
        return DateUtils.dateTimeNow(DateUtils.YYYY_MM_DD_HH_MM_SS)

    @staticmethod
    def dateTimeNow(format = YYYYMMDDHHMMSS):
        """
        根据指定格式获取当前日期时间，对应Java版本中的dateTimeNow方法（带参数版本）
        """
        return datetime.now().strftime(format)

    @staticmethod
    def dateTime(date=datetime.now()):
        """
        将日期对象按照指定格式（yyyy-MM-dd）转换为字符串，对应Java版本中的dateTime方法
        """
        return date.strftime(DateUtils.YYYY_MM_DD)

    @staticmethod
    def parseDateToStr(format, date):
        """
        将日期对象按照指定格式转换为字符串，对应Java版本中的parseDateToStr方法
        """
        return date.strftime(format)

    @staticmethod
    def dateTimeFormat(format, ts):
        """
        将指定格式的日期时间字符串转换为日期对象，对应Java版本中的dateTime方法（带两个参数版本）
        """
        try:
            return datetime.strptime(ts, format)
        except ValueError:
            raise ValueError(f"Invalid date format: {ts}")

    @staticmethod
    def datePath():
        """
        获取日期路径，格式为yyyy/MM/dd，对应Java版本中的datePath方法
        """
        return datetime.now().strftime("%Y/%M/%d")

    @staticmethod
    def parseDate(str_date):
        """
        日期型字符串转化为日期，尝试多种格式解析，对应Java版本中的parseDate方法
        """
        if str_date is None:
            return None
        for pattern in DateUtils.parse_patterns:
            try:
                return datetime.strptime(str_date, pattern)
            except ValueError:
                continue
        return None

    @staticmethod
    def getServerStartDate():
        """
        获取服务器启动时间，Python中可简单获取当前进程启动时间来模拟，对应Java版本中的getServerStartDate方法
        """
        return datetime.fromtimestamp(time.process_time())

    @staticmethod
    def timeDistance(end_date, start_date):
        """
        计算时间差，返回天、小时、分钟的表示形式，对应Java版本中的timeDistance方法
        """
        diff = (end_date - start_date).total_seconds()
        day = diff // (24 * 60 * 60)
        hour = (diff % (24 * 60 * 60)) // (60 * 60)
        minute = (diff % (60 * 60)) // 60
        return f"{int(day)}天{int(hour)}小时{int(minute)}分钟"

    @staticmethod
    def toDate(temporal_accessor):
        """
        将LocalDateTime或LocalDate类型转换为日期对象，对应Java版本中的toDate方法（根据Python实际情况调整实现）
        """
        if isinstance(temporal_accessor, datetime):
            return temporal_accessor
        elif isinstance(temporal_accessor, date):
            return datetime.combine(temporal_accessor, datetime.min.time())
        raise ValueError("Invalid input type for toDate method")

if __name__ == "__main__":
    # 测试getNowDate方法
    now_date = DateUtils.getNowDate()
    print(f"getNowDate方法获取的当前日期时间: {now_date}")

    # 测试getDate方法
    current_date = DateUtils.getDate()
    print(f"getDate方法获取的当前日期: {current_date}")

    # 测试getTime方法
    current_time = DateUtils.getTime()
    print(f"getTime方法获取的当前时间: {current_time}")

    # 测试dateTimeNow方法（无参数版本）
    current_datetime = DateUtils.dateTimeNow()
    print(f"dateTimeNow方法（无参数）获取的当前日期时间: {current_datetime}")

    # 测试dateTimeNow方法（带参数版本）
    custom_format_datetime = DateUtils.dateTimeNow("%Y-%m-%d %H:%M")
    print(f"dateTimeNow方法（带参数）获取的当前日期时间: {custom_format_datetime}")

    # 测试dateTime方法（将日期对象转换为字符串）
    test_date = datetime(2024, 1, 1)
    date_str = DateUtils.dateTime(test_date)
    print(f"dateTime方法将日期对象转换为字符串的结果: {date_str}")

    # 测试parseDateToStr方法
    another_date_str = DateUtils.parseDateToStr("%Y-%m-%d %H:%M:%S", datetime(2024, 1, 1, 12, 0, 0))
    print(f"parseDateToStr方法转换日期对象为字符串的结果: {another_date_str}")

    # 测试dateTime方法（将字符串转换为日期对象）
    try:
        parsed_date = DateUtils.dateTimeFormat("%Y-%m-%d", "2024-01-01")
        print(f"dateTime方法将字符串转换为日期对象的结果: {parsed_date}")
    except ValueError as e:
        print(f"dateTime方法测试失败，错误信息: {e}")

    # 测试datePath方法
    date_path = DateUtils.datePath()
    print(f"datePath方法获取的日期路径: {date_path}")

    # 测试dateTime方法（另一个无参数版本）
    date_time_str = DateUtils.dateTime()
    print(f"dateTime方法（另一个无参数版本）获取的日期时间字符串: {date_time_str}")

    # 测试parseDate方法
    test_date_str = "2024-01-01"
    parsed_date_obj = DateUtils.parseDate(test_date_str)
    print(f"parseDate方法解析日期字符串的结果: {parsed_date_obj}")

    # 测试getServerStartDate方法
    server_start_date = DateUtils.getServerStartDate()
    print(f"getServerStartDate方法获取的服务器启动时间: {server_start_date}")

    # 测试timeDistance方法
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 1, 2)
    time_diff = DateUtils.timeDistance(end_date, start_date)
    print(f"timeDistance方法计算的时间差: {time_diff}")

    # 测试toDate方法
    local_date = date(2024, 1, 1)
    converted_date = DateUtils.toDate(local_date)
    print(f"toDate方法转换LocalDate为日期对象的结果: {converted_date}")