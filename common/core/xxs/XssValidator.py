import re


class XssValidator:
    """
    自定义xss校验（模拟Java版本中的XssValidator类功能，简单判断是否含HTML标签来示意XSS校验）
    """
    HTML_PATTERN = r"<(\\S*?)[^>]*>.*?|<.*? />"

    @staticmethod
    def isValid(value):
        """
        判断输入的字符串是否有效（是否不包含HTML标签，模拟Java中isValid方法的逻辑，这里简化了参数，去除了ConstraintValidatorContext相关部分）
        """
        if not value:
            return True
        return not XssValidator.containsHtml(value)

    @staticmethod
    def containsHtml(value):
        """
        检查字符串中是否包含HTML标签，对应Java版本中的containsHtml方法
        """
        found_html = re.findall(XssValidator.HTML_PATTERN, value, re.DOTALL)
        return bool(found_html)

if __name__ == "__main__":
    # 示例使用
    text1 = "这是一段正常的文本"
    text2 = "<script>alert('xss');</script>"
    print(XssValidator.isValid(text1))
    print(XssValidator.isValid(text2))