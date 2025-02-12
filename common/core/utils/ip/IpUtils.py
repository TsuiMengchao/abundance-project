import socket
import re


class IpUtils:
    REGX_0_255 = r"(25[0-5]|2[0-4]\d|1\d{2}|[1-9]\d|\d)"
    REGX_IP = fr"(({REGX_0_255}\.){{3}}{REGX_0_255})"
    REGX_IP_WILDCARD = fr"(((\*\.){{3}}\*)|({REGX_0_255}(\.\*){{3}})|({REGX_0_255}\.{REGX_0_255})(\.\*){{2}}|(({REGX_0_255}\.){{3}}\*))"
    REGX_IP_SEG = fr"({REGX_IP}\-{REGX_IP})"

    @staticmethod
    def get_ip_addr():
        """
        获取客户端IP地址，尝试从常见的HTTP请求头中获取，若获取不到则使用默认方式获取
        """
        import requests
        try:
            response = requests.get('http://ifconfig.me/ip')
            return response.text.strip() if response.status_code == 200 else "unknown"
        except:
            return "unknown"

    @staticmethod
    def get_ip_addr_with_request(request):
        """
        从给定的HTTP请求对象中获取客户端IP地址
        """
        if request is None:
            return "unknown"
        headers = request.headers
        ip = headers.get('x-forwarded-for')
        if not ip or ip == "unknown":
            ip = headers.get('Proxy-Client-IP')
        if not ip or ip == "unknown":
            ip = headers.get('X-Forwarded-For')
        if not ip or ip == "unknown":
            ip = headers.get('WL-Proxy-Client-IP')
        if not ip or ip == "unknown":
            ip = headers.get('X-Real-IP')
        if not ip or ip == "unknown":
            ip = request.remote_addr
        return "127.0.0.1" if ip == "0:0:0:0:0:0:0:1" else IpUtils.get_multistage_reverse_proxy_ip(ip)

    @staticmethod
    def internal_ip(ip):
        """
        检查给定的IP地址是否为内部IP地址
        """
        addr = IpUtils.text_to_numeric_format_v4(ip)
        return IpUtils._internal_ip(addr) or ip == "127.0.0.1"

    @staticmethod
    def _internal_ip(addr):
        """
        辅助方法，检查字节形式的IP地址是否为内部IP地址
        """
        if addr is None or len(addr) < 2:
            return True
        b0, b1 = addr[0], addr[1]
        SECTION_1 = 0x0A
        SECTION_2 = 0xAC
        SECTION_3 = 0x10
        SECTION_4 = 0x1F
        SECTION_5 = 0xC0
        SECTION_6 = 0xA8
        if b0 == SECTION_1:
            return True
        elif b0 == SECTION_2 and SECTION_3 <= b1 <= SECTION_4:
            return True
        elif b0 == SECTION_5 and b1 == SECTION_6:
            return True
        return False

    @staticmethod
    def text_to_numeric_format_v4(text):
        """
        将IPv4地址转换成字节形式
        """
        if not text:
            return None
        parts = text.split('.')
        if len(parts) not in [1, 2, 3, 4]:
            return None
        try:
            result = []
            if len(parts) == 1:
                num = int(parts[0])
                if not (0 <= num <= 4294967295):
                    return None
                result.append(num >> 24 & 0xFF)
                result.append((num & 0xFFFFFF) >> 16 & 0xFF)
                result.append((num & 0xFFFF) >> 8 & 0xFF)
                result.append(num & 0xFF)
            elif len(parts) == 2:
                num1 = int(parts[0])
                if not (0 <= num1 <= 255):
                    return None
                result.append(num1 & 0xFF)
                num2 = int(parts[1])
                if not (0 <= num2 <= 16777215):
                    return None
                result.append(num2 >> 16 & 0xFF)
                result.append((num2 & 0xFFFF) >> 8 & 0xFF)
                result.append(num2 & 0xFF)
            elif len(parts) == 3:
                for i in range(2):
                    num = int(parts[i])
                    if not (0 <= num <= 255):
                        return None
                    result.append(num & 0xFF)
                num = int(parts[2])
                if not (0 <= num <= 65535):
                    return None
                result.append(num >> 8 & 0xFF)
                result.append(num & 0xFF)
            else:
                for part in parts:
                    num = int(part)
                    if not (0 <= num <= 255):
                        return None
                    result.append(num & 0xFF)
            return bytes(result)
        except ValueError:
            return None

    @staticmethod
    def get_host_ip():
        """
        获取本地IP地址
        """
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "127.0.0.1"

    @staticmethod
    def get_host_name():
        """
        获取本地主机名
        """
        try:
            return socket.gethostname()
        except:
            return "未知"

    @staticmethod
    def get_multistage_reverse_proxy_ip(ip):
        """
        从多级反向代理中获得第一个非unknown的IP地址
        """
        if ip and ',' in ip:
            ips = [sub_ip.strip() for sub_ip in ip.split(',')]
            for sub_ip in ips:
                if not IpUtils.is_unknown(sub_ip):
                    ip = sub_ip
                    break
        return ip[:255] if ip else ""

    @staticmethod
    def is_unknown(check_string):
        """
        检测给定字符串是否为未知（比如为空或者是'unknown'），多用于检测HTTP请求相关
        """
        return not check_string or check_string.lower() == "unknown"

    @staticmethod
    def is_ip(ip):
        """
        判断给定的字符串是否为合法的IP地址
        """
        return bool(re.match(IpUtils.REGX_IP, ip)) if ip else False

    @staticmethod
    def is_ip_wild_card(ip):
        """
        判断给定的字符串是否为IP地址或带 * 为间隔的通配符地址
        """
        return bool(re.match(IpUtils.REGX_IP_WILDCARD, ip)) if ip else False

    @staticmethod
    def ip_is_in_wild_card_no_check(ip_wild_card, ip):
        """
        检测参数是否在ip通配符里（简单比较，不做严格的格式校验等）
        """
        parts1 = ip_wild_card.split('.')
        parts2 = ip.split('.')
        for i in range(len(parts1)):
            if parts1[i]!= '*' and parts1[i]!= parts2[i]:
                return False
        return True

    @staticmethod
    def is_ip_segment(ip_seg):
        """
        判断是否为特定格式如:“10.10.10.1-10.10.10.99”的ip段字符串
        """
        return bool(re.match(IpUtils.REGX_IP_SEG, ip_seg)) if ip_seg else False

    @staticmethod
    def ip_is_in_net_no_check(ip_area, ip):
        """
        判断ip是否在指定网段中（简单逻辑比较，不做严格的边界等处理）
        """
        start, end = ip_area.split('-')
        start_parts = [int(x) for x in start.split('.')]
        end_parts = [int(x) for x in end.split('.')]
        ip_parts = [int(x) for x in ip.split('.')]
        for i in range(4):
            if start_parts[i] > end_parts[i]:
                start_parts[i], end_parts[i] = end_parts[i], start_parts[i]
        return all(start_parts[i] <= ip_parts[i] <= end_parts[i] for i in range(4))

    @staticmethod
    def is_matched_ip(filter, ip):
        """
        校验ip是否符合过滤串规则（支持后缀 '*' 通配、支持网段等格式）
        """
        if not filter or not ip:
            return False
        filters = filter.split(';')
        for f in filters:
            if IpUtils.is_ip(f) and f == ip:
                return True
            elif IpUtils.is_ip_wild_card(f) and IpUtils.ip_is_in_wild_card_no_check(f, ip):
                return True
            elif IpUtils.is_ip_segment(f) and IpUtils.ip_is_in_net_no_check(f, ip):
                return True
        return False

if __name__ == '__main__':
    # 测试get_ip_addr方法
    print("获取客户端IP地址（通用方式）:", IpUtils.get_ip_addr())

    # 模拟请求对象（简单示例，实际应用中根据具体框架等情况完善）
    class MockRequest:
        def __init__(self, headers, remote_addr):
            self.headers = headers
            self.remote_addr = remote_addr

    mock_headers = {
        'x-forwarded-for': '192.168.1.100',
        'Proxy-Client-IP': 'unknown',
        'X-Forwarded-For': '',
        'WL-Proxy-Client-IP': 'unknown',
        'X-Real-IP': 'unknown'
    }
    mock_request = MockRequest(mock_headers, '127.0.0.1')
    # 测试get_ip_addr_with_request方法
    print("获取客户端IP地址（从模拟请求对象获取）:", IpUtils.get_ip_addr_with_request(mock_request))

    # 测试internal_ip方法
    test_ip = "192.168.1.100"
    print(f"IP {test_ip} 是否为内部IP地址:", IpUtils.internal_ip(test_ip))

    # 测试text_to_numeric_format_v4方法
    ipv4_text = "192.168.1.1"
    print("将IP地址转换为字节形式:", IpUtils.text_to_numeric_format_v4(ipv4_text))

    # 测试get_host_ip方法
    print("获取本地IP地址:", IpUtils.get_host_ip())

    # 测试get_host_name方法
    print("获取本地主机名:", IpUtils.get_host_name())

    # 测试get_multistage_reverse_proxy_ip方法
    multi_ip = "192.168.1.100,unknown,192.168.1.101"
    print("从多级反向代理IP中获取有效IP:", IpUtils.get_multistage_reverse_proxy_ip(multi_ip))

    # 测试is_unknown方法
    check_str = "unknown"
    print(f"字符串 {check_str} 是否为未知:", IpUtils.is_unknown(check_str))

    # 测试is_ip方法
    ip_str = "192.168.1.1"
    print(f"字符串 {ip_str} 是否为合法IP地址:", IpUtils.is_ip(ip_str))

    # 测试is_ip_wild_card方法
    wild_card_ip = "192.168.*.*"
    print(f"字符串 {wild_card_ip} 是否为带通配符的IP地址:", IpUtils.is_ip_wild_card(wild_card_ip))

    # 测试ip_is_in_wild_card_no_check方法
    wild_card = "192.168.*.*"
    target_ip = "192.168.1.1"
    print(f"IP {target_ip} 是否在通配符IP {wild_card} 范围内:", IpUtils.ip_is_in_wild_card_no_check(wild_card, target_ip))

    # 测试is_ip_segment方法
    ip_seg = "192.168.1.1-192.168.1.100"
    print(f"字符串 {ip_seg} 是否为IP段字符串:", IpUtils.is_ip_segment(ip_seg))

    # 测试ip_is_in_net_no_check方法
    ip_area = "192.168.1.1-192.168.1.100"
    ip_to_check = "192.168.1.50"
    print(f"IP {ip_to_check} 是否在网段 {ip_area} 中:", IpUtils.ip_is_in_net_no_check(ip_area, ip_to_check))

    # 测试is_matched_ip方法
    filter_str = "192.168.1.1;192.168.*.*;192.168.1.1-192.168.1.100"
    ip_to_match = "192.168.1.50"
    print(f"IP {ip_to_match} 是否符合过滤串 {filter_str} 规则:", IpUtils.is_matched_ip(filter_str, ip_to_match))