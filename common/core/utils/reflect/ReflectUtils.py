import inspect
import functools


class ReflectUtils:
    @staticmethod
    def invoke_getter(obj, property_name):
        """
        调用Getter方法，支持多级，如：对象名.对象名.方法
        """
        parts = property_name.split('.')
        result = obj
        for part in parts:
            result = getattr(result, part)
        return result

    @staticmethod
    def invoke_setter(obj, property_name, value):
        """
        调用Setter方法，支持多级，如：对象名.对象名.方法
        """
        parts = property_name.split('.')
        target = obj
        for part in parts[:-1]:
            target = getattr(target, part)
        setattr(target, parts[-1], value)

    @staticmethod
    def get_field_value(obj, field_name):
        """
        直接读取对象属性值，无视私有修饰符，不经过getter函数
        """
        try:
            return getattr(obj, field_name)
        except AttributeError:
            print(f"在 [{obj.__class__.__name__}] 中，没有找到 [{field_name}] 字段")
            return None

    @staticmethod
    def set_field_value(obj, field_name, value):
        """
        直接设置对象属性值，无视私有修饰符，不经过setter函数
        """
        try:
            setattr(obj, field_name, value)
        except AttributeError:
            print(f"在 [{obj.__class__.__name__}] 中，没有找到 [{field_name}] 字段")

    @staticmethod
    def invoke_method(obj, method_name, *args, **kwargs):
        """
        直接调用对象方法，无视私有修饰符，同时匹配方法名+参数类型
        """
        method = ReflectUtils.get_accessible_method(obj, method_name, args)
        if method:
            return method(*args, **kwargs)
        print(f"在 [{obj.__class__.__name__}] 中，没有找到 [{method_name}] 方法")
        return None

    @staticmethod
    def invoke_method_by_name(obj, method_name, args):
        """
        直接调用对象方法，无视私有修饰符，只匹配函数名，如果有多个同名函数调用第一个
        """
        methods = [m for m in dir(obj) if callable(getattr(obj, m)) and m == method_name]
        if methods:
            method = getattr(obj, methods[0])
            # 类型转换（将参数数据类型转换为目标方法参数类型）
            sig = inspect.signature(method)
            bound_arguments = sig.bind(*args)
            bound_arguments.apply_defaults()
            return method(*bound_arguments.args, **bound_arguments.kwargs)
        print(f"在 [{obj.__class__.__name__}] 中，没有找到 [{method_name}] 方法")
        return None

    @staticmethod
    def get_accessible_method(obj, method_name, args):
        """
        循环查找对象的方法，匹配方法名+参数类型，找到后返回可调用的方法对象，若找不到则返回None
        """
        for cls in inspect.getmro(obj.__class__):
            try:
                method = cls.__dict__[method_name]
                if callable(method) and ReflectUtils.match_method_signature(method, args):
                    return functools.partial(method, obj)
            except KeyError:
                continue
        return None

    @staticmethod
    def match_method_signature(method, args):
        """
        判断方法的参数类型是否与传入的参数类型匹配
        """
        sig = inspect.signature(method)
        parameters = sig.parameters
        if len(parameters)!= len(args):
            return False
        for param_name, param in parameters.items():
            if not isinstance(args[param_name], param.annotation):
                return False
        return True

    @staticmethod
    def get_generic_type(cls, index=0):
        """
        通过反射，获得类定义中声明的父类的泛型参数的类型，如无法找到，返回object类型
        """
        bases = cls.__bases__
        if bases:
            base = bases[0]
            if hasattr(base, '__args__'):
                args = base.__args__
                if index < len(args):
                    return args[index]
        return object

    @staticmethod
    def get_user_class(instance):
        """
        获取真实类（处理类似被装饰器等情况影响的类），这里简单判断是否有特定装饰器标记，示例中暂简单处理，可根据实际情况扩展
        """
        return instance.__class__

if __name__ == '__main__':
    class MyClass:
        pass


    obj = MyClass()
    user_class = ReflectUtils.get_user_class(obj)
    print(user_class)