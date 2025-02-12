import traceback

class ThrowableUtil:


    @staticmethod
    def get_stack_trace(exc):
        """
        获取异常的堆栈信息
        """
        stack_trace = traceback.format_exc()
        return stack_trace

if __name__ == '__main__':
    def divide(a, b):
        try:
            result = a / b
            return result
        except ZeroDivisionError as e:
            stack_trace = ThrowableUtil.get_stack_trace(e)
            print(stack_trace)

    divide(10, 0)