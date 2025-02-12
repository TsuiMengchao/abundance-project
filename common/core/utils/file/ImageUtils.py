import urllib.request
import io
import logging


class ImageUtils:
    @staticmethod
    def get_image(image_path):
        """
        获取图片的字节数据
        """
        file_stream = ImageUtils.get_file(image_path)
        if file_stream:
            return file_stream.read()
        return None

    @staticmethod
    def get_file(image_path):
        """
        获取图片对应的输入流（Python中以类似文件对象形式体现）
        """
        try:
            file_bytes = ImageUtils.read_file(image_path)
            return io.BytesIO(file_bytes)
        except Exception as e:
            logging.error("获取图片异常 %s", e)
        return None

    @staticmethod
    def read_file(url):
        """
        读取文件（可以是网络地址对应的文件）为字节数据
        """
        in_stream = None
        try:
            if url.startswith("http://") or url.startswith("https://"):
                # 网络地址
                req = urllib.request.Request(url)
                req.add_header('User-Agent', 'Mozilla/5.0')  # 添加User-Agent头，避免部分网站限制访问
                url_connection = urllib.request.urlopen(req, timeout=30)
                in_stream = url_connection.getInputStream()
                return in_stream.read()
            else:
                # 本地文件路径情况，以二进制模式读取文件
                with open(url, 'rb') as file_obj:
                    return file_obj.read()
        except urllib.request.URLError as e:
            if hasattr(e, 'reason'):
                logging.error("网络连接失败: %s", e.reason)
            elif hasattr(e, 'code'):
                logging.error("服务器返回错误码: %s", e.code)
            return None
        except Exception as e:
            logging.error("访问文件异常: %s", e)
            return None
        finally:
            if in_stream:
                try:
                    in_stream.close()
                except:
                    pass

if __name__ == '__main__':
    # 测试读取网络图片
    image_url = "https://example.com/some_image.jpg"
    image_bytes = ImageUtils.get_image(image_url)
    if image_bytes:
        print("成功获取网络图片字节数据，长度:", len(image_bytes))
    else:
        print("获取网络图片失败")

    # 测试读取本地图片（假设本地有个test.jpg文件，需根据实际路径调整）
    local_image_path = "/path/to/test.jpg"
    local_image_bytes = ImageUtils.get_image(local_image_path)
    if local_image_bytes:
        print("成功获取本地图片字节数据，长度:", len(local_image_bytes))
    else:
        print("获取本地图片失败")