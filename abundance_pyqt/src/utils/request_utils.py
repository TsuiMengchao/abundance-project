# request_utils.py
import logging

import requests

response = None
logger = logging.getLogger(__name__)

class RequestUtils:
    @staticmethod
    def request(method, url, **kwargs):
        try:
            response = requests.request(method, url, **kwargs)
            response.raise_for_status()  # 如果响应状态码表示失败，则引发HTTPError

            if 'application/json' in response.headers.get('Content-Type', ''):
                try:
                    return response.json(), None
                except ValueError as json_err:
                    logger.error(f"JSON解析错误: {json_err}")
                    return response.text, f"JSON解析错误: {json_err}"
            elif 'image/png' in response.headers.get('Content-Type', ''):
                logger.debug(f"返回的数据是Content-Type: {response.headers.get('Content-Type')}格式")
                return response.content, None
            else:
                logger.debug(f"返回的数据不是JSON格式，Content-Type: {response.headers.get('Content-Type')}")
                return response.text, None
        except requests.exceptions.HTTPError as http_err:
            try:
                # 即使响应码失败，也尝试获取并返回返回值（以json格式尝试获取，如果不是json格式可能会再次报错，可按需调整）
                return response.json(), f"HTTP error occurred: {http_err}"
            except:
                # 如果获取json失败，返回文本内容（可以根据实际需求进一步细化处理，比如判断编码等情况）
                return response.text, f"HTTP error occurred: {http_err}"
        except Exception as err:
            return None, f"An error occurred: {err}"

    @staticmethod
    def get(url, params=None, data=None, headers=None, on_success=None, on_failure=None):
        result, error = RequestUtils.request("GET", url, params=params, data=data, headers=headers)
        if error:
            if on_failure:
                on_failure(error, result)
        else:
            if on_success:
                on_success(result)
        return result, error

    @staticmethod
    def post(url, params=None, data=None, json=None, headers=None, on_success=None, on_failure=None):
        result, error = RequestUtils.request("POST", url, params=params, data=data, json=json, headers=headers)
        if error:
            if on_failure:
                on_failure(error, result)
        else:
            if on_success:
                on_success(result)
        return result, error

    @staticmethod
    def put(url, params=None, data=None, json=None, headers=None, on_success=None, on_failure=None):
        result, error = RequestUtils.request("PUT", url, params=params, data=data, json=json, headers=headers)
        if error:
            if on_failure:
                on_failure(error, result)
        else:
            if on_success:
                on_success(result)
        return result, error

    @staticmethod
    def delete(url, params=None, data=None, headers=None, on_success=None, on_failure=None):
        result, error = RequestUtils.request("DELETE", url, params=params, data=data, headers=headers)
        if error:
            if on_failure:
                on_failure(error, result)
        else:
            if on_success:
                on_success(result)
        return result, error
