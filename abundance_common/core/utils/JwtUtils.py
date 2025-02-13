import jwt
from jwt import DecodeError
from typing import Dict, Optional

from abundance_common.core.constant.SecurityConstants import SecurityConstants


class JwtUtils:
    secret = "YOUR_SECRET_KEY"  # 这里假设一个密钥，实际应用中替换为真实的密钥，对应Java中的TokenConstants.SECRET

    @staticmethod
    def createToken(claims: Dict[str, object]) -> str:
        """
        从数据声明生成令牌，对应Java版本中的createToken方法
        """
        try:
            token = jwt.encode(claims, JwtUtils.secret, algorithm="HS512")
            return token
        except jwt.exceptions.InvalidTokenError as e:
            raise ValueError(f"生成令牌失败，原因: {e}") from e

    @staticmethod
    def parseToken(token: str) -> Dict[str, object]:
        """
        从令牌中获取数据声明，对应Java版本中的parseToken方法
        """
        try:
            claims = jwt.decode(token, JwtUtils.secret, algorithms=["HS512"])
            return claims
        except DecodeError as e:
            raise ValueError(f"解析令牌失败，原因: {e}") from e

    @staticmethod
    def getUserKey(token: str) -> Optional[str]:
        """
        根据令牌获取用户标识，对应Java版本中的getUserKey方法（接收令牌参数的版本）
        """
        claims = JwtUtils.parseToken(token)
        return JwtUtils.getValue(claims, SecurityConstants.USER_KEY)

    @staticmethod
    def getUserKey(claims: Dict[str, object]) -> Optional[str]:
        """
        根据令牌获取用户标识，对应Java版本中的getUserKey方法（接收身份信息参数的版本）
        """
        return JwtUtils.getValue(claims, SecurityConstants.USER_KEY)

    @staticmethod
    def getUserId(token: str) -> Optional[str]:
        """
        根据令牌获取用户ID，对应Java版本中的getUserId方法（接收令牌参数的版本）
        """
        claims = JwtUtils.parseToken(token)
        return JwtUtils.getValue(claims, SecurityConstants.DETAILS_USER_ID)

    @staticmethod
    def getUserId(claims: Dict[str, object]) -> Optional[str]:
        """
        根据身份信息获取用户ID，对应Java版本中的getUserId方法（接收身份信息参数的版本）
        """
        return JwtUtils.getValue(claims, SecurityConstants.DETAILS_USER_ID)

    @staticmethod
    def getUserName(token: str) -> Optional[str]:
        """
        根据令牌获取用户名，对应Java版本中的getUserName方法（接收令牌参数的版本）
        """
        claims = JwtUtils.parseToken(token)
        return JwtUtils.getValue(claims, SecurityConstants.DETAILS_USERNAME)

    @staticmethod
    def getUserName(claims: Dict[str, object]) -> Optional[str]:
        """
        根据身份信息获取用户名，对应Java版本中的getUserName方法（接收身份信息参数的版本）
        """
        return JwtUtils.getValue(claims, SecurityConstants.DETAILS_USERNAME)

    @staticmethod
    def getValue(claims: Dict[str, object], key: str) -> Optional[str]:
        """
        根据身份信息获取键值，对应Java版本中的getValue方法
        """
        if isinstance(claims, dict):
            return str(claims.get(key, ""))
        return None

if __name__ == "__main__":
    # 测试createToken方法
    claims = {"key1": "value1", "key2": 2}
    try:
        token = JwtUtils.createToken(claims)
        print(f"createToken方法生成的令牌: {token}")
    except ValueError as e:
        print(f"createToken方法测试失败，错误信息: {e}")

    # 测试parseToken方法
    if token:
        try:
            parsed_claims = JwtUtils.parseToken(token)
            print(f"parseToken方法解析令牌得到的数据声明: {parsed_claims}")
        except ValueError as e:
            print(f"parseToken方法测试失败，错误信息: {e}")

    # 测试getUserKey方法（通过令牌获取）
    if token:
        user_key_from_token = JwtUtils.getUserKey(token)
        print(f"getUserKey方法（通过令牌）获取的用户标识: {user_key_from_token}")

    # 测试getUserKey方法（通过身份信息获取）
    if parsed_claims:
        user_key_from_claims = JwtUtils.getUserKey(parsed_claims)
        print(f"getUserKey方法（通过身份信息）获取的用户标识: {user_key_from_claims}")

    # 测试getUserId方法（通过令牌获取）
    if token:
        user_id_from_token = JwtUtils.getUserId(token)
        print(f"getUserId方法（通过令牌）获取的用户ID: {user_id_from_token}")

    # 测试getUserId方法（通过身份信息获取）
    if parsed_claims:
        user_id_from_claims = JwtUtils.getUserId(parsed_claims)
        print(f"getUserId方法（通过身份信息）获取的用户ID: {user_id_from_claims}")

    # 测试getUserName方法（通过令牌获取）
    if token:
        user_name_from_token = JwtUtils.getUserName(token)
        print(f"getUserName方法（通过令牌）获取的用户名: {user_name_from_token}")

    # 测试getUserName方法（通过身份信息获取）
    if parsed_claims:
        user_name_from_claims = JwtUtils.getUserName(parsed_claims)
        print(f"getUserName方法（通过身份信息）获取的用户名: {user_name_from_claims}")

    # 测试getValue方法
    if parsed_claims:
        value = JwtUtils.getValue(parsed_claims, "key1")
        print(f"getValue方法获取的值: {value}")