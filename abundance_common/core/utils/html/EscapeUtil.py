import html
import re
from typing import Union


class EscapeUtil:
    RE_HTML_MARK = r"(<[^<]*?>)|(<[\s]*?/[^<]*?>)|(<[^<]*?/[\s]*?>)"

    @staticmethod
    def escape(text: Union[str, None]) -> str:
        """
        转义文本中的HTML字符为安全的字符
        """
        if text is None:
            return ""
        return html.escape(text)

    @staticmethod
    def unescape(content: Union[str, None]) -> str:
        """
        还原被转义的HTML特殊字符
        """
        if content is None:
            return ""
        return html.unescape(content)

    @staticmethod
    def clean(content: Union[str, None]) -> str:
        """
        清除所有HTML标签，但是不删除标签内的内容
        """
        if content is None:
            return ""
        pattern = re.compile(r"<[^>]*?>")
        return pattern.sub("", content)

    @staticmethod
    def encode(text: Union[str, None]) -> str:
        """
        Escape编码（这里使用Python内置的urllib.parse.quote的功能来模拟类似效果）
        """
        if text is None:
            return ""
        import urllib.parse
        return urllib.parse.quote(text)

    @staticmethod
    def decode(content: Union[str, None]) -> str:
        """
        Escape解码（对应urllib.parse.unquote功能来模拟）
        """
        if content is None:
            return ""
        import urllib.parse
        return urllib.parse.unquote(content)


if __name__ == "__main__":
    html_str = "<script>alert(1);</script>"
    escaped = EscapeUtil.escape(html_str)
    print("clean: ", EscapeUtil.clean(html_str))
    print("escape: ", escaped)
    print("unescape: ", EscapeUtil.unescape(escaped))