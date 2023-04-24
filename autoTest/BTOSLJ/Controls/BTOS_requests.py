# -*- coding:utf-8 -*-
import json
import json as myjson
import os
import time
import requests
from Commons.log import getlogger
from requests import exceptions
from decimal import Decimal
from jsonschema import validate
from jsonschema.exceptions import SchemaError, ValidationError


class RequestMain:

    def __init__(self, host=None):
        self.session = requests.session()
        self.logger = getlogger()
        self.host = host
        if (host == '10.166.0.70'):
            self.headers = {
                'Content-Type': 'application/json',
                "Authorization": 'Bearer ' + self.get_token()
            }
        if (host == '10.116.8.16:8520'):
            self.headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }

    def request_main(self, method, url, params=None, data=None, json=None, headers=None, **kwargs):
        """
            :param method: 请求方式
	        :param url: 请求地址
	        :param params: 字典作为参数增加到url中
			:param data: Request传参, 字典格式
	        :param json: Request传参, json格式
	        :param headers: 请求头，字典格式
	        :param kwargs: 若还有其他的参数，使用可变参数字典形式进行传递
	        :return: 响应内容的文本
	    """
        try:
            header = self.headers if headers == None else headers
            res = self.session.request(method, "http://" + self.host + url, params=params, data=data, json=json,
                                       headers=header, **kwargs)
        except exceptions.RequestException as e:
            self.logger.error("请求失败:", exc_info=True)
        else:
            if res.status_code == 200:
                t = Decimal(res.elapsed.total_seconds()).quantize(Decimal("0.001"), rounding="ROUND_HALF_UP")
                s = "警告:用时较长" if t >= 1 else ""
                self.logger.info(url + " 用时:{}s {}".format(t, s))
                return res
            else:
                if (params):
                    payload = params
                elif (data):
                    payload = data
                else:
                    payload = json
                self.logger.info("请求错误:%s 状态码:%s\n请求参数:\n%s\n响应内容:\n%s"
                                 % (url, res.status_code, self.format(payload), self.format(res)))

    def __del__(self):
        self.session.close()

    # 格式化json
    def format(self, res):
        if (type(res) != type(dict())):
            res = myjson.loads(res)
        return myjson.dumps(res, indent=4, ensure_ascii=False)

    def get_token(self):
        payload = {
            "little_girl": "BAISHIJUN",
            "little_boy": "q1234567!",
            "verification": "xxx"
        }
        header = {
            'Content-Type': 'application/json'
        }
        try:
            res = self.request_main("post", "/auth/saas/authorization/login/simple", headers=header, json=payload)
        except exceptions.RequestException as e:
            self.logger.error("获取token失败:", exc_info=True)
        else:
            return myjson.loads(res)["data"]["access_token"]

    def generate_schema(cls, data: dict):
        schema = {"type": "object", "properties": {}}
        for key, value in data.items():
            if isinstance(value, bool):
                schema["properties"][key] = {"type": "boolean"}
            elif isinstance(value, int):
                schema["properties"][key] = {"type": "integer"}
            elif isinstance(value, float):
                schema["properties"][key] = {"type": "number"}
            elif isinstance(value, str):
                schema["properties"][key] = {"type": "string"}
            elif isinstance(value, list):
                schema["properties"][key] = {"type": "array", "items": {}}
                if value:
                    item_schema = cls.generate_schema(value[0])
                    if item_schema:
                        schema["properties"][key]["items"] = item_schema
            elif isinstance(value, dict):
                schema["properties"][key] = cls.generate_schema(value)
        return schema

    def save_schema(self, data: dict, path: str):
        try:
            if (type(data) != type(dict())):
                data = myjson.loads(data)
            schema = self.generate_schema(data)
            with open(path, 'w', encoding='utf-8') as f:
                myjson.dump(schema, f, indent=4)
        except FileNotFoundError:
            self.logger.error("文件不存在:%s" % path, exc_info=True)
        else:
            return schema

    def load_json(self, path: str):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                model = json.load(f)
        except FileNotFoundError:
            self.logger.error("文件不存在:%s" % path, exc_info=True)
        else:
            return self.format(model)

    def check_json(self, res_json: dict, schema: dict):
        try:
            if (type(res_json) != type(dict())):
                res_json = json.loads(res_json)
            if (type(schema) != type(dict())):
                schema = json.loads(schema)
            validate(instance=res_json, schema=schema)
        except SchemaError:
            self.logger.error("schema格式错误, 提示信息:", exc_info=True, stack_info=False)
            return False
        except ValidationError:
            self.logger.error("响应数据不符合schema, 提示信息:", exc_info=True, stack_info=False)
            return False
        else:
            return True


if __name__ == "__main__":
    myrequest = RequestMain(host="10.116.8.16:8520")
    params = {
        "workdate": "2023-03-24",
        "tenant_id": "SIPGLJ"
    }

    res = myrequest.request_main("get", "/api/blj/DAYNIGHTWORKHOUR/DAY", params=params)
    schema = myrequest.generate_schema(myjson.loads(res))
    print(myrequest.format(schema))
    print(myrequest.check_json(res, schema))
    # myrequest.load_json("1.json")
