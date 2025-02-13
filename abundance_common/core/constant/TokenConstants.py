class TokenConstants:
    """
    Token的Key常量，对应Java版本中的TokenConstants类
    """
    # 令牌前缀
    PREFIX = "Bearer "
    # 令牌秘钥
    SECRET = "abcdefghijklmnopqrstuvwxyz"

if __name__ == "__main__":
    print(f"令牌前缀常量: {TokenConstants.PREFIX}")
    print(f"令牌秘钥常量: {TokenConstants.SECRET}")