# 模拟排除JSON敏感属性的类，对应Java中的PropertyPreExcludeFilter类
class PropertyPreExcludeFilter:
    def __init__(self):
        self.excludes = set()

    def addExcludes(self, filters):
        self.excludes.update(filters)

    def filter(self, obj):
        if isinstance(obj, dict):
            result = {}
            for key, value in obj.items():
                if key not in self.excludes:
                    result[key] = self.filter(value)
            return result
        elif isinstance(obj, list):
            return [self.filter(item) for item in obj]
        return obj