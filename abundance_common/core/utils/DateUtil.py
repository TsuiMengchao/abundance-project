from datetime import datetime, date, timedelta, timezone
import pytz


class DateUtil:
    """
    JDK 8新日期类格式化与字符串转换工具类的Python模拟实现，用于日期时间相关的格式转换、类型转换等操作
    """
    DFY_MD_HMS = "%Y-%m-%d %H:%M:%S"
    DFY_MD = "%Y-%m-%d"

    @staticmethod
    def get_time_stamp(local_datetime):
        """
        LocalDateTime转时间戳，将Python的datetime对象转换为对应的时间戳（以秒为单位）
        """
        return local_datetime.timestamp()

    @staticmethod
    def from_time_stamp(time_stamp):
        """
        时间戳转LocalDateTime，根据给定的时间戳创建对应的Python的datetime对象
        """
        return datetime.fromtimestamp(time_stamp, pytz.timezone('Asia/Shanghai'))

    @staticmethod
    def to_date(local_datetime):
        """
        LocalDateTime转Date，将Python的datetime对象转换为date对象（去除时间部分）
        """
        return local_datetime.date()

    @staticmethod
    def to_date_from_local_date(local_date):
        """
        LocalDate转Date，将Python的date对象转换为date对象（本身就是，这里保持一致）
        """
        return local_date

    @staticmethod
    def to_local_datetime(dt):
        """
        Date转LocalDateTime，将Python的date对象转换为包含当前时间的datetime对象（设置时间部分为当前时间）
        """
        return datetime.combine(dt, datetime.now().time())

    @staticmethod
    def local_datetime_format(local_datetime, pattern):
        """
        日期格式化，按照指定的格式将Python的datetime对象格式化为字符串
        """
        return local_datetime.strftime(pattern)

    @staticmethod
    def local_datetime_format_with_formatter(local_datetime, df):
        """
        日期格式化，按照给定的格式化器（字符串格式）将Python的datetime对象格式化为字符串
        """
        return local_datetime.strftime(df)

    @staticmethod
    def local_datetime_formatyMdHms(local_datetime):
        """
        日期格式化yyyy-MM-dd HH:mm:ss，按照固定格式将Python的datetime对象格式化为字符串
        """
        return local_datetime.strftime(DateUtil.DFY_MD_HMS)

    @staticmethod
    def local_datetime_formatyMd(local_datetime):
        """
        日期格式化yyyy-MM-dd，按照固定格式将Python的datetime对象格式化为字符串
        """
        return local_datetime.strftime(DateUtil.DFY_MD)

    @staticmethod
    def parse_local_datetime_format(local_datetime_str, pattern):
        """
        字符串转LocalDateTime，按照指定的格式将字符串解析为Python的datetime对象
        """
        return datetime.strptime(local_datetime_str, pattern)

    @staticmethod
    def parse_local_datetime_format_with_formatter(local_datetime_str, date_time_formatter):
        """
        字符串转LocalDateTime，按照给定的格式化器（字符串格式）将字符串解析为Python的datetime对象
        """
        return datetime.strptime(local_datetime_str, date_time_formatter)

    @staticmethod
    def parse_local_datetime_formatyMdHms(local_datetime_str):
        """
        字符串转LocalDateTime，按照固定格式yyyy-MM-dd HH:mm:ss将字符串解析为Python的datetime对象
        """
        return datetime.strptime(local_datetime_str, DateUtil.DFY_MD_HMS)

if __name__ == '__main__':
    if __name__ == "__main__":
        # 创建一个示例的datetime对象
        dt = datetime.now()
        print("原始datetime对象:", dt)

        # 测试get_time_stamp方法
        time_stamp = DateUtil.get_time_stamp(dt)
        print("转换为时间戳:", time_stamp)

        # 测试from_time_stamp方法
        new_dt = DateUtil.from_time_stamp(time_stamp)
        print("从时间戳转换回的datetime对象:", new_dt)

        # 测试local_datetime_formatyMdHms方法
        formatted_str = DateUtil.local_datetime_formatyMdHms(dt)
        print("格式化后的字符串（yyyy-MM-dd HH:mm:ss）:", formatted_str)

        # 测试parse_local_datetime_formatyMdHms方法
        parsed_dt = DateUtil.parse_local_datetime_formatyMdHms(formatted_str)
        print("从格式化字符串解析回的datetime对象:", parsed_dt)