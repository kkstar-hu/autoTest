import json
import requests
from Commons.log import getlogger
from requests import exceptions
from decimal import Decimal
from SLPTHF.Config import config

class RequestMain:
    def __init__(self, host=None, headers=None):
        self.session = requests.session()
        self.logger = getlogger()
        self.host = host
        self.header = headers

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
        data =data.encode('utf-8') if not data==None else None
        try:
            res = self.session.request(method, "http://" + self.host + url, params=params, data=data, json=json,
                                       headers=headers, **kwargs)
        except exceptions.RequestException as e:
            self.logger.error("请求失败:", exc_info=True)
        else:
            if res.status_code == 200:
                t = Decimal(res.elapsed.total_seconds()).quantize(Decimal("0.001"), rounding="ROUND_HALF_UP")
                s = "警告:用时较长" if t >= 1 else ""
                self.logger.info(method + ":" + url + " 用时:{}s {}".format(t, s))
            elif res.status_code == 500:
                if params:
                    payload = params
                elif json:
                    payload = json
                else:
                    payload = {}
                self.logger.error("%s:%s 状态码:%s\n请求参数:\n%s\n响应内容:\n%s"
                                  % (method, url, res.status_code, payload, res.text))
            else:
                self.logger.error("%s:%s 状态码:%s" % (method, url, res.status_code), exc_info=True)
            return res

    def __del__(self):
        self.session.close()

    # 格式化json
    def format(self, res):
        if not isinstance(res, dict):
            res = json.loads(res)
        return json.dumps(res, indent=4, ensure_ascii=False)

    def get_token(self):
        payload = {
            "little_girl": config.username,
            "little_boy": config.password
        }
        header = {
            'Content-Type': 'application/json'
        }
        try:
            res = self.request_main("POST", "/saas/authorization/login/simple", headers=header, json=payload)
        except exceptions.RequestException as e:
            self.logger.error("获取token失败:", exc_info=True)
        else:
            return json.loads(res.text)["data"]["access_token"]

if __name__ == '__main__':
    rm = RequestMain('10.166.0.190:9088')
    token = rm.get_token()
    print(token)