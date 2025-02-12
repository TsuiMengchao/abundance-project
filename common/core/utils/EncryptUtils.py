from Crypto.Cipher import DES
import binascii


class EncryptUtils:
    """
    加密工具类，模拟实现类似Java代码中EncryptUtils类的功能，用于对称加密（DES）和解密操作
    """
    # 相当于Java代码中的固定密钥相关参数
    STR_PARAM = "Passw0rd".encode('utf-8')
    # 设置加密模式和填充方式，对应Java代码中的 "DES/CBC/PKCS5Padding"
    MODE = DES.MODE_CBC

    @staticmethod
    def get_des_key_spec(source):
        """
        获取DES加密的密钥规范，这里简单返回固定的密钥字节串（对应Java代码中根据固定字符串生成密钥规范的逻辑）
        """
        if source is None or len(source) == 0:
            return None
        # 这里使用固定的密钥，实际应用中可根据需求调整
        key = "Passw0rd".encode('utf-8')
        return key

    @staticmethod
    def des_encrypt(source):
        """
        对称加密（DES）方法，对输入的源字符串进行加密并返回十六进制字符串表示的加密结果
        """
        key = EncryptUtils.get_des_key_spec(source)
        # 创建DES加密对象，使用CBC模式并传入初始向量（IV）
        cipher = DES.new(key, EncryptUtils.MODE, EncryptUtils.STR_PARAM)
        # 对源字符串进行填充，使其长度符合加密要求（这里简单使用空格填充示例，实际更严谨的做法可按规则填充）
        padded_source = source + (8 - len(source) % 8) * " "
        padded_source_bytes = padded_source.encode('utf-8')
        encrypted_bytes = cipher.encrypt(padded_source_bytes)
        return binascii.hexlify(encrypted_bytes).decode('utf-8').upper()

    @staticmethod
    def des_decrypt(source):
        """
        对称解密（DES）方法，对输入的十六进制字符串表示的加密数据进行解密并返回原始字符串
        """
        key = EncryptUtils.get_des_key_spec(source)
        cipher = DES.new(key, EncryptUtils.MODE, EncryptUtils.STR_PARAM)
        encrypted_bytes = binascii.unhexlify(source)
        decrypted_bytes = cipher.decrypt(encrypted_bytes)
        return decrypted_bytes.rstrip().decode('utf-8')

    @staticmethod
    def byte2hex(in_str):
        """
        将字节数组转换为十六进制字符串表示，类似Java代码中的byte2hex方法
        """
        return binascii.hexlify(in_str).decode('utf-8')

    @staticmethod
    def hex2byte(b):
        """
        将十六进制字符串表示的数据转换为字节数组，类似Java代码中的hex2byte方法
        """
        return binascii.unhexlify(b)

if __name__ == '__main__':
    source_str = "Hello, World!"
    encrypted_str = EncryptUtils.des_encrypt(source_str)
    print("加密后的字符串:", encrypted_str)
    decrypted_str = EncryptUtils.des_decrypt(encrypted_str)
    print("解密后的字符串:", decrypted_str)