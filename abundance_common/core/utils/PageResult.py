from typing import List, TypeVar


T = TypeVar('T')


class PageResult:
    """
    分页结果类，模拟实现类似Java代码中PageResult类的功能，用于封装分页数据（内容列表和总元素数量）
    """

    def __init__(self, content: List[T], total_elements: int):
        self.content = content
        self.total_elements = total_elements


class PageUtil:
    """
    分页工具类，模拟实现类似Java代码中PageUtil类的功能，实现各种分页相关操作
    """

    @staticmethod
    def paging(page: int, size: int, lst: List[T]) -> List[T]:
        """
        List分页，根据指定的页码和每页大小对输入的列表进行分页，返回对应页的数据列表
        """
        start_index = page * size
        end_index = page * size + size
        if start_index >= len(lst):
            return []
        elif end_index >= len(lst):
            return lst[start_index:]
        return lst[start_index:end_index]

    @staticmethod
    def to_page(page):
        """
        Page数据处理（这里假设page对象有类似的属性和方法获取内容和总元素数量，可根据实际情况调整），
        将分页数据转换为PageResult对象，预防类似redis反序列化报错等情况（具体需根据实际使用场景细化）
        """
        content = page.content if hasattr(page, 'content') else []
        total_elements = page.total_elements if hasattr(page, 'total_elements') else 0
        return PageResult(content, total_elements)

    @staticmethod
    def to_page_custom(lst: List[T], total_elements: int) -> PageResult:
        """
        自定义分页，根据给定的列表数据和总元素数量创建并返回PageResult对象
        """
        return PageResult(lst, total_elements)

    @staticmethod
    def no_data() -> PageResult:
        """
        返回空数据，创建一个表示没有数据的PageResult对象（内容为None，总元素数量为0）
        """
        return PageResult(None, 0)

if __name__ == '__main__':
    # 示例数据列表
    data_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    # 进行分页操作，假设每页显示3条数据，获取第2页数据
    page_size = 3
    page_num = 0
    paged_data = PageUtil.paging(page_num, page_size, data_list)
    print("分页后的数据:", paged_data)

    # 模拟一个简单的分页对象（这里简单使用字典模拟，实际可能是数据库查询返回的分页对象等）
    page_obj = {'content': [11, 12, 13], 'total_elements': 15}
    page_result = PageUtil.to_page(page_obj)
    print("转换后的PageResult对象:", page_result.content, page_result.total_elements)

    # 使用自定义分页创建PageResult对象
    custom_page_result = PageUtil.to_page_custom([14, 15], 2)
    print("自定义分页的PageResult对象:", custom_page_result.content, custom_page_result.total_elements)

    # 获取空数据的PageResult对象
    empty_page_result = PageUtil.no_data()
    print("空数据的PageResult对象:", empty_page_result.content, empty_page_result.total_elements)