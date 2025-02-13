from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
import base64


class RsaUtils:
    SRC = "123456"

    @staticmethod
    def generate_key_pair():
        """
        构建RSA密钥对
        """
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=1024,
            backend=default_backend()
        )
        public_key = private_key.public_key()

        private_key_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        public_key_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        return {
            "public_key": public_key_pem.decode('utf-8'),
            "private_key": private_key_pem.decode('utf-8')
        }

    @staticmethod
    def encrypt_by_public_key(public_key_text, text):
        """
        公钥加密
        """
        public_key = serialization.load_pem_public_key(
            public_key_text.encode('utf-8'),
            backend=default_backend()
        )
        encrypted_text = public_key.encrypt(
            text.encode('utf-8'),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return base64.b64encode(encrypted_text).decode('utf-8')

    @staticmethod
    def decrypt_by_private_key(private_key_text, text):
        """
        私钥解密
        """
        private_key = serialization.load_pem_private_key(
            private_key_text.encode('utf-8'),
            password=None,
            backend=default_backend()
        )
        decrypted_text = private_key.decrypt(
            base64.b64decode(text),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return decrypted_text.decode('utf-8')

    @staticmethod
    def encrypt_by_private_key(private_key_text, text):
        """
        私钥加密
        """
        private_key = serialization.load_pem_private_key(
            private_key_text.encode('utf-8'),
            password=None,
            backend=default_backend()
        )
        encrypted_text = private_key.sign(
            text.encode('utf-8'),
            padding.PSS(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return base64.b64encode(encrypted_text).decode('utf-8')

    @staticmethod
    def decrypt_by_public_key(public_key_text, signature, text):
        """
        公钥解密
        """
        public_key = serialization.load_pem_public_key(
            public_key_text.encode('utf-8'),
            backend=default_backend()
        )
        try:
            public_key.verify(
                signature,
                base64.b64decode(text),
                padding.PSS(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except:
            return None

    @staticmethod
    def test1(key_pair):
        """
        公钥加密私钥解密
        """
        print("***************** 公钥加密私钥解密开始 *****************")
        text1 = RsaUtils.encrypt_by_public_key(key_pair["public_key"], RsaUtils.SRC)
        text2 = RsaUtils.decrypt_by_private_key(key_pair["private_key"], text1)
        print("加密前：", RsaUtils.SRC)
        print("加密后：", text1)
        print("解密后：", text2)
        if RsaUtils.SRC == text2:
            print("解密字符串和原始字符串一致，解密成功")
        else:
            print("解密字符串和原始字符串不一致，解密失败")
        print("***************** 公钥加密私钥解密结束 *****************")

    @staticmethod
    def test2(key_pair):
        """
        私钥加密公钥解密
        """
        print("***************** 私钥加密公钥解密开始 *****************")
        text1 = RsaUtils.encrypt_by_private_key(key_pair["private_key"], RsaUtils.SRC)
        text2 = RsaUtils.decrypt_by_public_key(key_pair["public_key"], text1, RsaUtils.SRC)
        print("加密前：", RsaUtils.SRC)
        print("加密后：", text1)
        print("解密后：", text2)
        if RsaUtils.SRC == text2:
            print("解密字符串和原始字符串一致，解密成功")
        else:
            print("解密字符串和原始字符串不一致，解密失败")
        print("***************** 私钥加密公钥解密结束 *****************")


if __name__ == "__main__":
    rsa_utils = RsaUtils()
    key_pair = rsa_utils.generate_key_pair()
    print("公钥：", key_pair["public_key"])
    print("私钥：", key_pair["private_key"])
    rsa_utils.test1(key_pair)
    rsa_utils.test2(key_pair)