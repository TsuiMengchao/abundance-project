import os

import validators


class ValidationUtil:
    @staticmethod
    def is_null(obj, entity, parameter, value):
        """
        验证对象是否为空，为空则抛出异常
        """
        if obj is None:
            msg = f"{entity} 不存在: {parameter} is {value}"
            raise ValueError(msg)

    @staticmethod
    def is_email(email):
        """
        验证是否为邮箱
        """
        return validators.email(email)

    @staticmethod
    def is_url(url):
        return validators.url(url)

    @staticmethod
    def is_file_path(path):
        """
        验证是否为有效的文件地址
        """
        try:
            # 检查路径是否存在
            if os.path.exists(path):
                # 检查路径是否指向一个文件
                return os.path.isfile(path)
            return False
        except Exception:
            return False

if __name__ == '__main__':

    # 测试is_null方法
    try:
        ValidationUtil.is_null(None, "用户对象", "user_id", "None")
    except ValueError as e:
        print(e)

    # 测试is_email方法
    email_address = "example@example.com"
    print(ValidationUtil.is_email(email_address))

    url = "http://example.com"
    print(ValidationUtil.is_url(url))