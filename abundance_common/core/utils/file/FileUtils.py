import os
import uuid
from datetime import datetime
import hashlib
import mimetypes
import os
import mimetypes
import urllib.parse


class FileUtils:
    """
    文件工具类，模拟实现类似Java代码中FileUtil类的功能，扩展相关文件操作功能
    """
    # 系统临时目录，Python中获取临时目录并添加路径分隔符（注意不同系统的分隔符差异，这里以常见的'/'为例，实际使用时可适配）
    SYS_TEM_DIR = os.path.join(os.getenv('TEMP', '/tmp'), '')
    # 定义GB的计算常量（以字节为单位）
    GB = 1024 ** 3
    # 定义MB的计算常量（以字节为单位）
    MB = 1024 ** 2
    # 定义KB的计算常量（以字节为单位）
    KB = 1024
    # 格式化小数，用于文件大小格式化显示
    DF = "{:.2f}".format

    IMAGE = "图片"
    TXT = "文档"
    MUSIC = "音乐"
    VIDEO = "视频"
    OTHER = "其他"

    SLASH = '/'
    BACKSLASH = '\\'
    FILENAME_PATTERN = r"[a-zA-Z0-9_\-\|\.\u4e00-\u9fa5]+"

    @staticmethod
    def get_extension_name(file_name):
        """
        获取文件扩展名，不带 '.'
        """
        return os.path.splitext(file_name)[1][1:] if file_name else ""

    @staticmethod
    def get_file_name_no_ex(file_name):
        """
        获取不带扩展名的文件名
        """
        return os.path.splitext(file_name)[0] if file_name else ""

    @staticmethod
    def get_size(size_in_bytes):
        """
        文件大小转换，根据文件字节大小转换为合适的单位（GB、MB、KB或B）并格式化显示
        """
        if size_in_bytes >= FileUtils.GB:
            return f"{FileUtils.DF(size_in_bytes / FileUtils.GB)}GB"
        elif size_in_bytes >= FileUtils.MB:
            return f"{FileUtils.DF(size_in_bytes / FileUtils.MB)}MB"
        elif size_in_bytes >= FileUtils.KB:
            return f"{FileUtils.DF(size_in_bytes / FileUtils.KB)}KB"
        return f"{size_in_bytes}B"

    @staticmethod
    def input_stream_to_file(input_stream, file_name):
        """
        将输入流转换为文件，保存到临时目录
        """
        file_path = os.path.join(FileUtils.SYS_TEM_DIR, file_name)
        with open(file_path, 'wb') as output_file:
            while True:
                data = input_stream.read(8192)
                if not data:
                    break
                output_file.write(data)
        return file_path

    @staticmethod
    def upload(multipart_file, file_path):
        """
        将文件上传到指定路径，按照一定规则生成文件名（包含时间戳等信息）并保存文件
        """
        now = datetime.now().strftime('%Y%m%d%H%M%S%f')
        # 过滤非法文件名
        file_name = FileUtils.get_file_name_no_ex(FileUtils.verify_filename(multipart_file.filename))
        file_suffix = FileUtils.get_extension_name(multipart_file.filename)
        file_full_name = f"{file_name}-{now}.{file_suffix}"
        full_path = os.path.join(file_path, file_full_name)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        try:
            with open(full_path, 'wb') as f:
                f.write(multipart_file.read())
            return full_path
        except Exception as e:
            print(f"Error uploading file: {e}")
            return None

    @staticmethod
    def download_excel(data_list):
        """
        导出Excel文件，将数据列表转换为Excel并保存到临时目录，返回文件路径
        """
        import pandas as pd
        file_name = f"{str(uuid.uuid4())}.xlsx"
        file_path = os.path.join(FileUtils.SYS_TEM_DIR, file_name)
        df = pd.DataFrame(data_list)
        df.to_excel(file_path, index=False)
        return file_path

    @staticmethod
    def get_file_type(file_type):
        """
        根据文件类型判断所属分类（图片、文档、音乐、视频或其他）
        """
        documents = ["txt", "doc", "pdf", "ppt", "pps", "xlsx", "xls", "docx"]
        music = ["mp3", "wav", "wma", "mpa", "ram", "ra", "aac", "aif", "m4a"]
        video = ["avi", "mpg", "mpe", "mpeg", "asf", "wmv", "mov", "qt", "rm", "mp4", "flv", "m4v", "webm", "ogv", "ogg"]
        image = ["bmp", "dib", "pcp", "dif", "wmf", "gif", "jpg", "tif", "eps", "psd", "cdr", "iff", "tga", "pcd", "mpt",
                 "png", "jpeg"]
        if file_type in image:
            return FileUtils.IMAGE
        elif file_type in documents:
            return FileUtils.TXT
        elif file_type in music:
            return FileUtils.MUSIC
        elif file_type in video:
            return FileUtils.VIDEO
        return FileUtils.OTHER

    @staticmethod
    def check_size(max_size, size):
        """
        检查文件大小是否超出规定大小，超出则抛出异常
        """
        if size > max_size:
            raise ValueError(f"文件超出规定大小: {max_size} bytes")

    @staticmethod
    def check(file_path_1, file_path_2):
        """
        判断两个文件是否相同，通过比较文件的MD5哈希值来判断
        """
        md5_1 = FileUtils.get_md5(file_path_1)
        md5_2 = FileUtils.get_md5(file_path_2)
        return md5_1 == md5_2

    @staticmethod
    def check_by_md5(md5_1, md5_2):
        """
        通过给定的两个MD5哈希值判断文件是否相同
        """
        return md5_1 == md5_2

    @staticmethod
    def get_byte(file_path):
        """
        获取文件内容的字节数据
        """
        with open(file_path, 'rb') as file:
            return file.read()

    @staticmethod
    def get_md5(file_path):
        """
        获取文件的MD5哈希值，用于文件内容校验等操作
        """
        hash_md5 = hashlib.md5()
        with open(file_path, 'rb') as file:
            for chunk in iter(lambda: file.read(4096), b''):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    @staticmethod
    def download_file(file_path, delete_on_exit=False):
        """
        下载文件，将文件内容读取并返回，可选择下载后是否删除文件
        """
        file_name = os.path.basename(file_path)
        with open(file_path, 'rb') as f:
            content = f.read()
        if delete_on_exit:
            os.remove(file_path)
        return content

    @staticmethod
    def verify_filename(file_name):
        """
        验证并过滤非法的文件名，去除特殊字符、控制字符、非法路径等，限制文件名长度等操作
        """
        # 过滤掉特殊字符
        file_name = file_name.replace('\\', '_').replace('/', '_').replace(':', '_').replace('*', '_').replace('?', '_') \
            .replace('"', '_').replace('<', '_').replace('>', '_').replace('|', '_').replace(' ', '_')

        # 不允许文件名超过255（在Mac和Linux中）或260（在Windows中）个字符
        max_length = 255 if not os.name.startswith('Windows') else 260
        if len(file_name) > max_length:
            file_name = file_name[:max_length]

        # 使用mimetypes库猜测文件类型
        file_type, _ = mimetypes.guess_type(file_name)
        if file_type:
            file_type_main, file_type_sub = file_type.split('/')
            file_name = file_name.replace('.', '_') + '.' + file_type_sub
        return file_name

    @staticmethod
    def write_bytes(file_path, output_stream):
        """
        输出指定文件的字节数据到给定的输出流
        """
        try:
            with open(file_path, 'rb') as file_obj:
                while True:
                    b = file_obj.read(1024)
                    if not b:
                        break
                    output_stream.write(b)
        except OSError as e:
            raise e

    @staticmethod
    def delete_file(file_path):
        """
        删除指定的文件，如果文件存在且是文件类型则删除，返回删除是否成功的布尔值
        """
        file_obj = os.path.isfile(file_path)
        if file_obj and os.path.exists(file_path):
            return os.remove(file_path) is None
        return False

    @staticmethod
    def is_valid_filename(filename):
        """
        文件名称验证，判断文件名是否符合指定的正则表达式模式
        """
        import re
        return bool(re.match(FileUtils.FILENAME_PATTERN, filename))

    @staticmethod
    def check_allow_download(resource):
        """
        检查文件是否可下载，禁止目录上跳级别以及判断文件类型是否在允许的扩展名列表内
        """
        if ".." in resource:
            return False
        file_type = os.path.splitext(resource)[-1].lower()
        allowed_extensions = mimetypes.types_map.keys()
        return file_type in allowed_extensions

    @staticmethod
    def set_file_download_header(request, file_name):
        """
        根据不同的浏览器类型对下载文件名进行重新编码
        """
        user_agent = request.headers.get('USER-AGENT', '')
        if 'MSIE' in user_agent:
            # IE浏览器
            encoded_name = urllib.parse.quote(file_name, encoding='utf-8')
            return encoded_name.replace('+', ' ')
        elif 'Firefox' in user_agent:
            # 火狐浏览器
            return file_name.encode('ISO8859-1').decode('ISO8859-1')
        elif 'Chrome' in user_agent:
            # google浏览器
            return urllib.parse.quote(file_name, encoding='utf-8')
        else:
            # 其它浏览器
            return urllib.parse.quote(file_name, encoding='utf-8')

    @staticmethod
    def get_name(file_path):
        """
        返回文件名，去除路径中的最后一个分隔符及之前的部分
        """
        if file_path is None:
            return None
        file_path = file_path.rstrip(FileUtils.SLASH + FileUtils.BACKSLASH)
        return os.path.basename(file_path)

    @staticmethod
    def is_file_separator(c):
        """
        判断字符是否为Windows或者Linux（Unix）文件分隔符
        """
        return c == FileUtils.SLASH or c == FileUtils.BACKSLASH

    @staticmethod
    def set_attachment_response_header(response, real_file_name):
        """
        设置附件响应头，对文件名进行合适的编码处理后设置到响应头中
        """
        percent_encoded_file_name = urllib.parse.quote(real_file_name, encoding='utf-8').replace('+', '%20')
        content_disposition_value = f'attachment; filename="{percent_encoded_file_name}";filename*=utf-8\'\'{percent_encoded_file_name}'
        response.headers['Content-disposition'] = content_disposition_value
        response.headers['download-filename'] = percent_encoded_file_name

    @staticmethod
    def percent_encode(s):
        """
        百分号编码工具方法，对字符串进行URL编码并处理空格等特殊字符
        """
        return urllib.parse.quote(s, encoding='utf-8').replace('+', '%20')




    
if __name__ == "__main__":
    # 测试get_extension_name方法
    file_name = "example.jpg"
    extension = FileUtils.get_extension_name(file_name)
    print("测试get_extension_name方法，文件扩展名:", extension)

    # 测试get_file_name_no_ex方法
    file_name_with_ext = "document.pdf"
    file_name_no_ex = FileUtils.get_file_name_no_ex(file_name_with_ext)
    print("测试get_file_name_no_ex方法，不带扩展名的文件名:", file_name_no_ex)

    # 测试get_size方法
    file_size = 1024 * 1024  # 1MB
    size_str = FileUtils.get_size(file_size)
    print("测试get_size方法，文件大小格式化显示:", size_str)

    # 测试get_file_type方法
    file_type = "jpg"
    file_type_result = FileUtils.get_file_type(file_type)
    print("测试get_file_type方法，文件类型分类:", file_type_result)

    # 测试check_size方法（模拟超出大小情况，会抛出异常）
    try:
        max_size = FileUtils.MB
        size = 2 * FileUtils.MB
        FileUtils.check_size(max_size, size)
    except ValueError as e:
        print("测试check_size方法，异常信息:", e)

    # 测试check方法（需要准备两个相同或不同的测试文件路径）
    file_path_1 = "file1.txt"
    file_path_2 = "file2.txt"
    are_same = FileUtils.check(file_path_1, file_path_2)
    print("测试check方法，文件是否相同:", are_same)

    # 测试download_file方法
    file_path_to_download = "test.txt"
    content = FileUtils.download_file(file_path_to_download)
    print("测试download_file方法，下载文件内容长度:", len(content))

    # 测试download_excel方法（简单构造数据列表示例）
    data_list = [{"col1": "value1", "col2": "value2"}]
    excel_file_path = FileUtils.download_excel(data_list)
    print("测试download_excel方法，导出的Excel文件路径:", excel_file_path)


    # 测试write_bytes方法
    file_path = "test.txt"  # 这里替换为实际存在的文件路径，用于读取字节数据
    output_file_path = "output.txt"  # 输出字节数据的目标文件路径，可按需调整
    try:
        with open(output_file_path, 'wb') as output_stream:
            FileUtils.write_bytes(file_path, output_stream)
        print("write_bytes方法测试：文件字节数据写入成功")
    except Exception as e:
        print(f"write_bytes方法测试：写入文件出现错误: {str(e)}")

    # 测试delete_file方法
    file_to_delete = "test.txt"  # 替换为要测试删除的实际文件路径
    result = FileUtils.delete_file(file_to_delete)
    if result:
        print("delete_file方法测试：文件删除成功")
    else:
        print("delete_file方法测试：文件删除失败")

    # 测试is_valid_filename方法
    filename = "test_file.txt"  # 替换为要测试的文件名
    result = FileUtils.is_valid_filename(filename)
    print(f"is_valid_filename方法测试：文件名验证结果: {result}")

    # 测试check_allow_download方法
    resource = "test_file.txt"  # 替换为要测试的资源文件名
    result = FileUtils.check_allow_download(resource)
    print(f"check_allow_download方法测试：文件是否可下载检查结果: {result}")

    # 模拟请求头（简单示例，可按需调整）
    mock_request_headers = {
        "USER-AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }


    class MockRequest:
        def __init__(self, headers):
            self.headers = headers


    mock_request = MockRequest(mock_request_headers)
    # 测试set_file_download_header方法
    file_name = "测试文件.txt"
    encoded_name = FileUtils.set_file_download_header(mock_request, file_name)
    print(f"set_file_download_header方法测试：文件名编码结果: {encoded_name}")

    # 测试get_name方法
    file_path = "/path/to/test_file.txt"  # 替换为实际的文件路径
    file_name = FileUtils.get_name(file_path)
    print(f"get_name方法测试：获取到的文件名: {file_name}")

    # 测试is_file_separator方法
    char_to_test = FileUtils.SLASH  # 可以替换为要测试的字符，比如FileUtils.BACKSLASH
    result = FileUtils.is_file_separator(char_to_test)
    print(f"is_file_separator方法测试：是否为文件分隔符测试结果: {result}")


    # 测试set_attachment_response_header方法
    # 简单模拟响应对象（仅为测试设置相关属性，非完整的HTTP响应模拟）
    class MockResponse:
        def __init__(self):
            self.headers = {}


    response = MockResponse()
    real_file_name = "重要文件.txt"
    FileUtils.set_attachment_response_header(response, real_file_name)
    print(f"set_attachment_response_header方法测试：响应头设置完成，可查看响应头信息：{response.headers}")

    # 测试percent_encode方法
    s = "包含空格的字符串"
    encoded_s = FileUtils.percent_encode(s)
    print(f"percent_encode方法测试：百分号编码结果: {encoded_s}")