import re


class SqlUtil:
    SQL_REGEX = r"\u000B|and |extractvalue|updatexml|sleep|exec |insert |select |delete |update |drop |count |chr |mid |master |truncate |char |declare |or |union |like |+|/*|user\(\)"
    SQL_PATTERN = r"[a-zA-Z0-9_ \,\.]+$"
    ORDER_BY_MAX_LENGTH = 500

    @staticmethod
    def escape_order_by_sql(value):
        """
        检查字符，防止注入绕过，针对ORDER BY部分进行验证和长度限制检查
        """
        if value and not SqlUtil.is_valid_order_by_sql(value):
            raise ValueError("参数不符合规范，不能进行查询")
        if len(value) > SqlUtil.ORDER_BY_MAX_LENGTH:
            raise ValueError("参数已超过最大限制，不能进行查询")
        return value

    @staticmethod
    def is_valid_order_by_sql(value):
        """
        验证order by语法是否符合规范，使用正则表达式匹配
        """
        return bool(re.match(SqlUtil.SQL_PATTERN, value))

    @staticmethod
    def filter_keyword(value):
        """
        SQL关键字检查，防止SQL注入风险
        """
        if not value:
            return
        sql_keywords = re.split(r"\|", SqlUtil.SQL_REGEX)
        for sql_keyword in sql_keywords:
            if sql_keyword.strip() in value.lower():
                raise ValueError("参数存在SQL注入风险")

if __name__ == "__main__":
    # 测试 escape_order_by_sql 方法
    order_by_value_1 = "column1, column2"
    try:
        result_1 = SqlUtil.escape_order_by_sql(order_by_value_1)
        print(f"escape_order_by_sql测试通过，返回值: {result_1}")
    except ValueError as e:
        print(f"escape_order_by_sql测试失败，错误信息: {e}")

    order_by_value_2 = "column1; DROP TABLE"
    try:
        result_2 = SqlUtil.escape_order_by_sql(order_by_value_2)
        print(f"escape_order_by_sql测试通过，返回值: {result_2}")
    except ValueError as e:
        print(f"escape_order_by_sql测试失败，错误信息: {e}")

    long_order_by_value = "a" * 501
    try:
        result_3 = SqlUtil.escape_order_by_sql(long_order_by_value)
        print(f"escape_order_by_sql测试通过，返回值: {result_3}")
    except ValueError as e:
        print(f"escape_order_by_sql测试失败，错误信息: {e}")

    # 测试 is_valid_order_by_sql 方法
    valid_value = "column1, column2"
    print(f"is_valid_order_by_sql测试，输入 {valid_value}，结果: {SqlUtil.is_valid_order_by_sql(valid_value)}")

    invalid_value = "column1; DROP TABLE"
    print(f"is_valid_order_by_sql测试，输入 {invalid_value}，结果: {SqlUtil.is_valid_order_by_sql(invalid_value)}")

    # 测试 filter_keyword 方法
    safe_value = "name = 'John' AND age > 20"
    try:
        SqlUtil.filter_keyword(safe_value)
        print(f"filter_keyword测试通过，输入 {safe_value} 无SQL注入风险")
    except ValueError as e:
        print(f"filter_keyword测试失败，错误信息: {e}")

    risky_value = "SELECT * FROM users WHERE 1 = 1; DROP TABLE users"
    try:
        SqlUtil.filter_keyword(risky_value)
        print(f"filter_keyword测试通过，输入 {risky_value} 无SQL注入风险")
    except ValueError as e:
        print(f"filter_keyword测试失败，错误信息: {e}")