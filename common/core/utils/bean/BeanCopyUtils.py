class BeanCopyUtils:
    """
    用于复制对象或集合属性的工具类，模拟实现类似Java代码中BeanCopyUtils的功能
    """

    @staticmethod
    def copy_object(source, target):
        """
        复制对象，将source对象的属性复制到target类型的新对象中（这里简单模拟类似Java的Bean复制，假设属性为字典形式）

        :param source: 源对象（这里可以是字典等类似结构）
        :param target: 目标对象类型（Python中可以是类或者字典等期望的结构类型）
        :return: 复制属性后的目标对象实例
        """
        try:
            if source is None:
                return None
            # 如果target是类，创建实例，这里简单假设类可以无参初始化，若不行需调整构造方式
            if isinstance(target, type):
                result = target()
            else:
                result = target.copy()
            for key, value in source.items():
                setattr(result, key, value)
            return result
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def copy_list(source, target):
        """
        拷贝集合，将源集合中的每个元素（对象）属性复制到目标类型的新对象中，并组成新的集合返回

        :param source: 源集合（列表，其中元素可以是字典等类似结构对象）
        :param target: 目标对象类型（Python中可以是类或者字典等期望的结构类型）
        :return: 复制属性后的目标对象组成的列表
        """
        result_list = []
        if source and len(source) > 0:
            for element in source:
                copied_element = BeanCopyUtils.copy_object(element, target)
                result_list.append(copied_element)
        return result_list


if __name__ == "__main__":
    # 测试copy_object方法，以字典作为示例数据类型
    source_dict = {'name': 'Alice', 'age': 25}
    target_dict_type = dict
    copied_dict = BeanCopyUtils.copy_object(source_dict, target_dict_type)
    print("测试copy_object复制字典:")
    print(copied_dict)

    # 测试copy_object方法，以自定义类作为示例数据类型
    class Person:
        def __init__(self):
            self.name = None
            self.age = None

    source_person = {'name': 'Bob', 'age': 30}
    target_person_type = Person
    copied_person = BeanCopyUtils.copy_object(source_person, target_person_type)
    print("测试copy_object复制自定义类对象:")
    print(f"姓名: {copied_person.name}, 年龄: {copied_person.age}")

    # 测试copy_list方法，以字典列表作为示例数据类型
    source_list_of_dicts = [{'name': 'Charlie', 'age': 35}, {'name': 'David', 'age': 40}]
    target_dict_type_for_list = dict
    copied_list_of_dicts = BeanCopyUtils.copy_list(source_list_of_dicts, target_dict_type_for_list)
    print("测试copy_list复制字典列表:")
    print(copied_list_of_dicts)

    # 测试copy_list方法，以自定义类列表作为示例数据类型
    source_list_of_persons = [{'name': 'Eve', 'age': 45}, {'name': 'Frank', 'age': 50}]
    target_person_type_for_list = Person
    copied_list_of_persons = BeanCopyUtils.copy_list(source_list_of_persons, target_person_type_for_list)
    print("测试copy_list复制自定义类对象列表:")
    for person in copied_list_of_persons:
        print(f"姓名: {person.name}, 年龄: {person.age}")