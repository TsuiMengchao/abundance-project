from Crypto.Cipher import AES
import base64


class AesEncryptUtils:
    """
    加密工具类
    """
    KEY = "mcx_abundance_24".encode('utf-8')

    @staticmethod
    def pad(s):
        """
        对需要加密的内容进行填充，使其长度符合AES加密要求
        """
        block_size = AES.block_size
        return s + (block_size - len(s) % block_size) * chr(block_size - len(s) % block_size).encode('utf-8')

    @staticmethod
    def unpad(s):
        """
        对解密后的内容去除填充部分
        """
        return s[:-s[-1]]

    @staticmethod
    def aes_encrypt(password):
        """
        AES加密
        :param password: 密码
        :return: 密文
        """
        password = password.encode('utf-8')
        cipher = AES.new(AesEncryptUtils.KEY, AES.MODE_ECB)
        encrypted_text = cipher.encrypt(AesEncryptUtils.pad(password))
        return base64.b64encode(encrypted_text).decode('utf-8')

    @staticmethod
    def validate(target, target1):
        """
        校验两个内容经过加密后是否一致
        :param target: 密文
        :param target1: 原文
        :return: 校验结果
        """
        encrypted_target = AesEncryptUtils.aes_encrypt(target1)
        return target.lower() == encrypted_target.lower()


if __name__ == "__main__":
    encrypted_result = AesEncryptUtils.aes_encrypt("123456")
    print(encrypted_result)
    print(AesEncryptUtils.validate(encrypted_result, "123456"))
