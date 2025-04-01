from abundance_pyqt.src.utils.request_utils import RequestUtils

BASE_URL = "https://api.example.com"

def create_resource(data, headers=None, on_success=None, on_failure=None):
    url = f"{BASE_URL}/resource"
    return RequestUtils.post(url, json=data, headers=headers, on_success=on_success, on_failure=on_failure)

def read_resource(resource_id, data=None, headers=None, on_success=None, on_failure=None):
    url = f"{BASE_URL}/resource/{resource_id}"
    return RequestUtils.get(url, data=data, headers=headers, on_success=on_success, on_failure=on_failure)

def update_resource(resource_id, data, headers=None, on_success=None, on_failure=None):
    url = f"{BASE_URL}/resource/{resource_id}"
    return RequestUtils.put(url, json=data, headers=headers, on_success=on_success, on_failure=on_failure)

def delete_resource(resource_id, data=None, headers=None, on_success=None, on_failure=None):
    url = f"{BASE_URL}/resource/{resource_id}"
    return RequestUtils.delete(url, data=data, headers=headers, on_success=on_success, on_failure=on_failure)

# 测试
if __name__ == "__main__":
    def on_success(result):
        print("请求成功:", result)

    def on_failure(error, result=None):
        print("请求失败:", error)
        print("失败请求体：", result)

    # 创建资源
    new_resource = {
        "name": "Example Resource",
        "value": "This is an example"
    }
    create_resource(new_resource, on_success=on_success, on_failure=on_failure)

    # 读取资源
    resource_id = 1
    read_resource(resource_id, on_success=on_success, on_failure=on_failure)

    # 更新资源
    updated_resource = {
        "name": "Updated Resource",
        "value": "This is an updated example"
    }
    update_resource(resource_id, updated_resource, on_success=on_success, on_failure=on_failure)

    # 删除资源
    delete_resource(resource_id, on_success=on_success, on_failure=on_failure)
