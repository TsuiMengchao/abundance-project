from pydantic import BaseModel, ValidationError
from typing import Type, Any


class BeanValidators:
    @staticmethod
    def validate_with_exception(model: Type[BaseModel], data: Any):
        """
        使用pydantic对数据进行验证，不符合模型定义则抛出异常
        """
        try:
            model(**data)
        except ValidationError as e:
            raise ValueError(e)

if __name__ == '__main__':

    class UserModel(BaseModel):
        name: str
        age: int


    data = {"name": "Alice", "age": "twenty"}  # 这里age的值不符合int类型要求
    try:
        BeanValidators.validate_with_exception(UserModel, data)
    except ValueError as e:
        print(f"验证出现错误: {e}")