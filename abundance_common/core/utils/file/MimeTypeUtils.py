class MimeTypeUtils:
    IMAGE_PNG = "image/png"
    IMAGE_JPG = "image/jpg"
    IMAGE_JPEG = "image/jpeg"
    IMAGE_BMP = "image/bmp"
    IMAGE_GIF = "image/gif"
    IMAGE_EXTENSION = ["bmp", "gif", "jpg", "jpeg", "png"]
    FLASH_EXTENSION = ["swf", "flv"]
    MEDIA_EXTENSION = ["swf", "flv", "mp3", "wav", "wma", "wmv", "mid", "avi", "mpg", "asf", "rm", "rmvb"]
    VIDEO_EXTENSION = ["mp4", "avi", "rmvb"]
    DEFAULT_ALLOWED_EXTENSION = [
        # 图片
        "bmp", "gif", "jpg", "jpeg", "png",
        # word excel powerpoint
        "doc", "docx", "xls", "xlsx", "ppt", "pptx", "html", "htm", "txt",
        # 压缩文件
        "rar", "zip", "gz", "bz2",
        # 视频格式
        "mp4", "avi", "rmvb",
        # pdf
        "pdf"
    ]

    @staticmethod
    def get_extension(prefix):
        """
        根据媒体类型前缀获取对应的文件扩展名
        """
        extension_mapping = {
            MimeTypeUtils.IMAGE_PNG: "png",
            MimeTypeUtils.IMAGE_JPG: "jpg",
            MimeTypeUtils.IMAGE_JPEG: "jpeg",
            MimeTypeUtils.IMAGE_BMP: "bmp",
            MimeTypeUtils.IMAGE_GIF: "gif"
        }
        return extension_mapping.get(prefix, "")

if __name__ == '__main__':
    # 测试get_extension方法
    media_type = MimeTypeUtils.IMAGE_PNG
    extension = MimeTypeUtils.get_extension(media_type)
    print(f"媒体类型 {media_type} 对应的扩展名是: {extension}")

    media_type = "unknown_type"
    extension = MimeTypeUtils.get_extension(media_type)
    print(f"媒体类型 {media_type} 对应的扩展名是: {extension}")