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
        '''
        if(host == '10.166.0.70'):
            self.headers = {
            'Content-Type': 'application/json',
            "Authorization": 'Bearer '+ self.get_token()
        }
        '''
        self.host = host
        #self.host == '10.116.8.16:8520'
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
            t1 = time.time()
            res = self.session.request(method, "http://"+self.host+url, params=params, data=data, json=json, headers=header, **kwargs)
            t2 = time.time()
        except exceptions.RequestException as e:
            self.logger.error("请求失败:", exc_info = True)
        else:
            if res.status_code == 200:
                t = Decimal(t2 - t1).quantize(Decimal("0.001"), rounding ="ROUND_HALF_UP")
                self.logger.info(url + " 耗时:%ss"%t)
                return res.text
            else:
                if(params):
                    payload = params
                elif(data):
                    payload = data
                else:
                    payload = json
                self.logger.info("请求错误:%s 状态码:%s\n请求参数:\n%s\n响应内容:\n%s"
                                 %(url, res.status_code, self.format(payload), self.format(res)))


    def __del__(self):
        self.session.close()


    # 格式化json
    def format(self, res):
        if(type(res) == type(dict())):
            return myjson.dumps(res, indent=4)
        return myjson.dumps(res.json(), indent=4)


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
            self.logger.error("获取token失败:", exc_info = True)
        else:
            return myjson.loads(res)["data"]["access_token"]


    def get_object_data(self, dict_data):
        # 外层dict
        schema_data = {}
        # 遍历字典中的key
        for dict_data_k in dict_data.keys():
            # 如果value是字符串/数字/布尔值/小数/None,则直接存入schema_data
            if type(dict_data[dict_data_k]) in (str, int, bool, float, list):
                if type(dict_data[dict_data_k]) is str:
                    schema_data[dict_data_k] = {"type": "string"}
                if type(dict_data[dict_data_k]) is int:
                    schema_data[dict_data_k] = {"type": "integer"}
                if type(dict_data[dict_data_k]) is bool:
                    schema_data[dict_data_k] = {"type": "boolean"}
                if type(dict_data[dict_data_k]) is float:
                    schema_data[dict_data_k] = {"type": "number"}
                if type(dict_data[dict_data_k]) is list:
                    this = {"type": "array", "items" : None }
                    for i in dict_data[dict_data_k]:
                        this["items"]=(self.generate_schema(data=i, flag=True))
                    schema_data[dict_data_k] = this
            elif dict_data[dict_data_k] is None:
                schema_data[dict_data_k] = {"type": "null"}
                continue
            elif type(dict_data[dict_data_k]) == dict:
                # 递归
                schema_temp = {"type": "object", 'properties': self.get_object_data(dict_data[dict_data_k])}
                schema_data[dict_data_k] = schema_temp
            else:
                print(dict_data[dict_data_k] == None)
        return schema_data


    def generate_schema(self, data, path=None, flag=False):
        # 固定外层kv
        if(type(data) != type(dict())):
            data = json.loads(data)
        if(flag):
            return {'type': "object", "required": [], 'properties': self.get_object_data(data)}
        else:
            schema = {'type': "object", "required": [], 'properties': self.get_object_data(data)}
            with open(path, mode='w', encoding='utf-8') as f:
                myjson.dump(schema, f, ensure_ascii=False, sort_keys=False, indent=4, separators=(',',': '))
            return schema


    def load_json(self, path):
        try:
            with open(path,'r',encoding='utf-8') as f:
                model=json.load(f)
        except FileNotFoundError:
            self.logger.error("文件不存在:%s"%path, exc_info=True)
        else:
            return self.format(model)


    def check_json(self, res_json : dict, schema : dict):
        try:
            if(type(res_json) != type(dict())):
                res_json = json.loads(res_json)
            validate(instance = res_json, schema = schema)
        except SchemaError as e:
            self.logger.info("schema格式错误, 错误位置:{}, 提示信息:{}"
                             .format("-->".join([i for i in e.path if i]), e.message))
            return False
        except ValidationError as e:
            self.logger.info("响应数据不符合schema, 错误字段:{}, 提示信息:{}"
                             .format("-->".join([i for i in e.path if i]), e.message))
            return False
        else:
            return True




if __name__ == "__main__":
    myrequest = RequestMain(host = "http://10.116.8.16:8520")
    params = {
        "workdate": "2023-03-24",
        "tenant_id": "SIPGLJ"
    }

    res = myrequest.request_main("get","/api/blj/DAYNIGHTWORKHOUR/DAY", params = params)
    schema = myrequest.generate_schema(res, "1.json")
    print(myrequest.check_json(res, schema))
    myrequest.load_json("1.json")


