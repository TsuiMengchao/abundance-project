class StrFormatter:
    """
    字符串格式化，对应Java版本中的StrFormatter类
    """
    EMPTY_JSON = "{}"
    C_BACKSLASH = '\\'
    C_DELIM_START = '{'
    C_DELIM_END = '}'

    @staticmethod
    def format(str_pattern, *arg_array):
        """
        格式化字符串，按照顺序将字符串模板中的占位符 {} 替换为参数，支持转义字符的处理
        """
        if not str_pattern or not arg_array:
            return str_pattern

        sbuf = []
        handled_position = 0
        arg_index = 0
        while arg_index < len(arg_array):
            delim_index = str_pattern.find(StrFormatter.EMPTY_JSON, handled_position)
            if delim_index == -1:
                if handled_position == 0:
                    return str_pattern
                else:
                    sbuf.append(str_pattern[handled_position:])
                    return "".join(sbuf)
            else:
                if delim_index > 0 and str_pattern[delim_index - 1] == StrFormatter.C_BACKSLASH:
                    if delim_index > 1 and str_pattern[delim_index - 2] == StrFormatter.C_BACKSLASH:
                        # 转义符之前还有一个转义符，占位符依旧有效
                        sbuf.append(str_pattern[handled_position:delim_index - 1])
                        sbuf.append(str(arg_array[arg_index]))
                        handled_position = delim_index + 2
                    else:
                        # 占位符被转义
                        arg_index -= 1
                        sbuf.append(str_pattern[handled_position:delim_index - 1])
                        sbuf.append(StrFormatter.C_DELIM_START)
                        handled_position = delim_index + 1
                else:
                    # 正常占位符
                    sbuf.append(str_pattern[handled_position:delim_index])
                    sbuf.append(str(arg_array[arg_index]))
                    handled_position = delim_index + 2
                arg_index += 1

        sbuf.append(str_pattern[handled_position:])
        return "".join(sbuf)


if __name__ == "__main__":
    # 示例使用
    print(StrFormatter.format("this is {} for {}", "a", "b"))
    print(StrFormatter.format("this is \\{} for {}", "a", "b"))
    print(StrFormatter.format("this is \\\\{} for {}", "a", "b"))