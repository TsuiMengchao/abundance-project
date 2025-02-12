import logging
import functools

class Slf4j:
    def __init__(self, cls):
        """
        在初始化时接收被装饰的类，用于后续添加日志记录器相关属性
        """
        self.cls = cls
        # 获取类所在模块的日志记录器，并添加到类属性中，属性名为 'log'
        self.cls.log = logging.getLogger(self.cls.__module__)

    def __call__(self, *args, **kwargs):
        """
        使得类实例化的过程能正常进行，当创建类的实例时会调用这个方法
        """
        return self.cls(*args, **kwargs)

if __name__ == '__main__':
    import logging
    import logging.config

    # 配置Python的logging模块基本信息（模拟Java中配置日志级别、格式等，这里简单配置输出到控制台）
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


    @Slf4j
    class MyClass:
        def my_method(self):
            self.log.info("在MyClass的my_method中记录的日志，使用模拟的@Slf4j装饰器注入日志记录器后记录")


    my_obj = MyClass()
    my_obj.my_method()