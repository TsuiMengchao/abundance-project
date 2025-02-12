import abc
import threading


class CallBack(metaclass=abc.ABCMeta):
    """
    针对某些初始化方法，模拟实现类似Java代码中CallBack接口的功能，
    可提交一个回调任务，在特定条件后进行回调使用
    """

    @abc.abstractmethod
    def executor(self):
        """
        回调执行方法，子类必须实现该抽象方法
        """
        pass

    def get_call_back_name(self):
        """
        返回本回调任务名称，默认使用当前线程ID和类名组成
        """
        return f"{threading.current_thread().ident}:{self.__class__.__name__}"

if __name__ == '__main__':
    class MyCallBack(CallBack):
        def executor(self):
            print("执行我的回调任务逻辑")


    my_callback = MyCallBack()
    print(my_callback.get_call_back_name())
    my_callback.executor()