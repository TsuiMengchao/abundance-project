import re
from typing import Dict, List, Union


class HTMLFilter:
    def __init__(self):
        self.vAllowed = {
            "a": ["href", "target"],
            "img": ["src", "width", "height", "alt"],
            "b": [],
            "strong": [],
            "i": [],
            "em": []
        }
        self.vSelfClosingTags = ["img"]
        self.vNeedClosingTags = ["a", "b", "strong", "i", "em"]
        self.vDisallowed = []
        self.vAllowedProtocols = ["http", "mailto", "https"]
        self.vProtocolAtts = ["src", "href"]
        self.vRemoveBlanks = ["a", "b", "strong", "i", "em"]
        self.vAllowedEntities = ["amp", "gt", "lt", "quot"]
        self.stripComment = True
        self.encodeQuotes = True
        self.alwaysMakeTags = False
        # 初始化vTagCounts为一个空字典
        self.vTagCounts = {}

    def filter(self, input_text):
        """
        对输入的可能包含HTML的文本进行过滤，去除无效或受限的HTML内容
        """
        input_text = self.escape_comments(input_text)
        input_text = self.balance_html(input_text)
        input_text = self.check_tags(input_text)
        input_text = self.process_remove_blanks(input_text)
        return input_text

    def escape_comments(self, s):
        """
        对HTML注释内容进行转义处理
        """
        pattern = re.compile("<!--(.*?)-->", re.DOTALL)
        return pattern.sub(lambda m: f"<!--{self.html_special_chars(m.group(1))}-->", s)

    def balance_html(self, s):
        """
        根据配置处理HTML标签的平衡，如尝试形成HTML标签或转义孤立的尖括号等
        """
        if self.alwaysMakeTags:
            s = re.sub("^>", "", s)
            s = re.sub("<([^>]*?)(?=<|$)", r"<\1>", s)
            s = re.sub("(^|>)([^<]*?)(?=>)", r"\1<\2", s)
        else:
            s = re.sub("<([^>]*?)(?=<|$)", r"&lt;\1", s)
            s = re.sub("(^|>)([^<]*?)(?=>)", r"\1\2&gt;<", s)
            s = re.sub("<>", "", s)
        return s

    def check_tags(self, s):
        """
        检查HTML标签，处理开始标签、结束标签以及相关属性等
        """
        pattern = re.compile("<(.*?)>", re.DOTALL)
        result = []
        tag_counts = {}
        for match in pattern.finditer(s):
            tag_content = match.group(1)
            processed_tag = self.process_tag(tag_content)
            result.append(processed_tag)
            # 更新标签计数
            start_tag_match = re.match(r"^([a-z0-9]+)(.*?)(/?)$", tag_content, re.IGNORECASE)
            if start_tag_match:
                tag_name = start_tag_match.group(1).lower()
                if tag_name in self.vTagCounts:
                    tag_counts[tag_name] = tag_counts.get(tag_name, 0) + (1 if processed_tag.startswith("<") else -1)
        # 根据标签计数添加结束标签
        for tag_name, count in tag_counts.items():
            if count > 0:
                result.extend([f"</{tag_name}>"] * count)
        return "".join(result)

    def process_remove_blanks(self, s):
        """
        处理需要移除空白内容的标签（如空的 <a></a> 或 <a /> 形式的标签）
        """
        for tag in self.vRemoveBlanks:
            s = re.sub(f"<{tag}(\\s[^>]*)?></{tag}>", "", s)
            s = re.sub(f"<{tag}(\\s[^>]*)?/>", "", s)
        return s

    def process_tag(self, s):
        """
        处理单个HTML标签，包括检查标签是否允许、处理属性等
        """
        # 处理结束标签
        end_tag_match = re.match(r"^/([a-z0-9]+)", s, re.IGNORECASE)
        if end_tag_match:
            tag_name = end_tag_match.group(1).lower()
            if self.allowed(tag_name) and tag_name not in self.vSelfClosingTags:
                if tag_name in self.vTagCounts and self.vTagCounts[tag_name] > 0:
                    self.vTagCounts[tag_name] -= 1
                    return f"</{tag_name}>"
        # 处理开始标签
        start_tag_match = re.match(r"^([a-z0-9]+)(.*?)(/?)$", s, re.IGNORECASE)
        if start_tag_match:
            tag_name = start_tag_match.group(1).lower()
            tag_body = start_tag_match.group(2)
            tag_ending = start_tag_match.group(3)
            if self.allowed(tag_name):
                params = []
                quoted_attrs_match = re.findall(r"([a-z0-9]+)=([\"'])(.*?)\2", tag_body, re.IGNORECASE)
                unquoted_attrs_match = re.findall(r"([a-z0-9]+)(=)([^\"\s']+)", tag_body, re.IGNORECASE)
                all_attrs = quoted_attrs_match + unquoted_attrs_match
                for attr_name, _, attr_value in all_attrs:
                    attr_name = attr_name.lower()
                    if self.allowed_attribute(tag_name, attr_name):
                        if attr_name in self.vProtocolAtts:
                            attr_value = self.process_param_protocol(attr_value)
                        params.append(f' {attr_name}="{attr_value}"')
                if tag_name in self.vSelfClosingTags:
                    tag_ending = " /"
                if tag_name in self.vNeedClosingTags:
                    tag_ending = ""
                if tag_ending == "" or tag_ending is None:
                    if tag_name not in self.vTagCounts:
                        self.vTagCounts[tag_name] = 0
                    self.vTagCounts[tag_name] += 1
                else:
                    tag_ending = " /"
                return f"<{tag_name}{''.join(params)}{tag_ending}>"
            return ""
        # 处理注释（如果不剥离注释且匹配到注释格式）
        comment_match = re.match(r"^!--(.*)--$", s, re.IGNORECASE)
        if not self.stripComment and comment_match:
            return f"<{comment_match.group()}>"
        return ""

    def process_param_protocol(self, s):
        """
        处理属性中的协议相关内容，检查协议是否允许，不允许则转换为本地锚链接
        """
        pattern = re.compile(r"^([^:]+):", re.IGNORECASE)
        match = pattern.match(s)
        if match:
            protocol = match.group(1).lower()
            if protocol not in self.vAllowedProtocols:
                s = "#" + s[len(protocol) + 1:]
                if s.startswith("#//"):
                    s = "#" + s[len("#//"):]
        return s

    def html_special_chars(self, s):
        """
        将HTML中的特殊字符转换为对应的实体编码
        """
        s = s.replace("&", "&amp;")
        s = s.replace('"', "&quot;")
        s = s.replace("<", "&lt;")
        s = s.replace(">", "&gt;")
        return s

    def allowed(self, name):
        """
        检查标签名称是否被允许（不在禁止列表且在允许列表中，允许列表为空时视为允许所有）
        """
        return (not self.vAllowed) or (name in self.vAllowed and name not in self.vDisallowed)

    def allowed_attribute(self, name, param_name):
        """
        检查标签的属性是否被允许（标签被允许且属性在该标签的允许属性列表中，允许列表为空时视为允许所有）
        """
        return self.allowed(name) and (not self.vAllowed or param_name in self.vAllowed[name])

if __name__ == '__main__':
    html_filter = HTMLFilter()
    input_html = "<script>alert('XSS');</script><a href='http://example.com'>Link</a><img src='invalid://source' />"
    filtered_html = html_filter.filter(input_html)
    print(filtered_html)