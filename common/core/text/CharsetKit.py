import codecs
import sys


class CharsetKit:
    """
    字符集工具类，对应Java版本中的CharsetKit类
    """
    # ISO-8859-1
    ISO_8859_1 = "ISO-8859-1"
    # UTF-8
    UTF_8 = "UTF-8"
    # GBK
    GBK = "GBK"

    @staticmethod
    def charset(charset):
        """
        转换为Charset对象（在Python中简单对应相应的编码名称字符串，这里模拟返回对应的编码名称），
        若传入为空则返回默认字符集编码名称，对应Java版本中的charset方法
        """
        if charset is None:
            return sys.getdefaultencoding()
        return charset

    @staticmethod
    def convert(source, srcCharset, destCharset):
        """
        转换字符串的字符集编码，对应Java版本中的convert方法
        """
        if srcCharset is None:
            srcCharset = CharsetKit.ISO_8859_1
        if destCharset is None:
            destCharset = CharsetKit.UTF_8
        if not source or srcCharset == destCharset:
            return source
        try:
            return codecs.decode(codecs.encode(source, srcCharset), destCharset)
        except UnicodeDecodeError:
            print(f"转换字符集编码时出现Unicode解码错误，源字符集: {srcCharset}，目标字符集: {destCharset}")
            return source
        except UnicodeEncodeError:
            print(f"转换字符集编码时出现Unicode编码错误，源字符集: {srcCharset}，目标字符集: {destCharset}")
            return source

    @staticmethod
    def systemCharset():
        """
        返回系统字符集编码，对应Java版本中的systemCharset方法
        """
        return sys.getdefaultencoding()


if __name__ == "__main__":
    # 示例使用
    source_str = "测试字符串"
    converted_str = CharsetKit.convert(source_str, CharsetKit.ISO_8859_1, CharsetKit.UTF_8)
    print(f"转换后的字符串: {converted_str}")
    print(f"系统字符集编码: {CharsetKit.systemCharset()}")
    print(f"获取默认字符集编码（模拟charset方法）: {CharsetKit.charset(None)}")