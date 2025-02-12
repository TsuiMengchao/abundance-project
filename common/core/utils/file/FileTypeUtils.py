import os
import magic  # 需要安装python-magic库


class FileTypeUtils:
    @staticmethod
    def get_file_type(file_obj):
        """
        获取文件类型，通过文件名获取后缀（不含'.'），如果传入的是文件对象则获取其文件名再处理
        """
        if file_obj is None:
            return ""
        file_name = file_obj if isinstance(file_obj, str) else file_obj.name
        separator_index = file_name.rfind('.')
        if separator_index < 0:
            return ""
        return file_name[separator_index + 1:].lower()

    @staticmethod
    def get_extension(multipart_file):
        """
        获取文件名的后缀，先尝试从原始文件名获取，若为空则从文件的Content-Type获取
        """
        original_filename = multipart_file.filename
        extension = os.path.splitext(original_filename)[-1][1:].lower() if original_filename else ""
        if not extension:
            content_type = multipart_file.content_type
            if content_type:
                extension = content_type.split('/')[-1]
        return extension

    @staticmethod
    def get_file_extend_name(photo_bytes):
        """
        通过文件字节码判断文件类型，返回对应的后缀（不含'.'）
        """
        try:
            file_type = magic.from_buffer(photo_bytes, mime=True)
            if file_type:
                return file_type.split('/')[-1].lower()
            return "unknown"
        except:
            return "unknown"

if __name__ == '__main__':
    # 测试get_file_type方法
    file_path = "test.txt"
    print(FileTypeUtils.get_file_type(file_path))


    # 模拟MultipartFile对象（简单示例，实际应用中根据具体框架等情况更完善）
    class MockMultipartFile:
        def __init__(self, filename, content_type):
            self.filename = filename
            self.content_type = content_type


    multipart_file = MockMultipartFile("test.jpg", "image/jpeg")
    print(FileTypeUtils.get_extension(multipart_file))

    # 测试get_file_extend_name方法
    with open('test.jpg', 'rb') as f:
        photo_bytes = f.read()
    print(FileTypeUtils.get_file_extend_name(photo_bytes))