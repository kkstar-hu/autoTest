import requests



class RequestHandler:


    def __init__(self):
        """session管理器"""
        self.session = requests.session()

    def visit(self, method, url, params=None, data=None, json=None, headers=None, **kwargs):
        return self.session.request(method, url, params=params, data=data, json=json, headers=headers, **kwargs)

    def close_session(self):
        """关闭session"""
        self.session.close()


if __name__ == '__main__':
    # 以下是测试代码
    # post请求接口
    url = 'http://apserver.cloudtos.com/api/auth'
    Body= {
        "useraccount": "admin",
        "password": "ECB004AB0C9F3A86675A7A67822D8A31",
        "ExtendProperties" : {"OP_TERMCD":"XICT"}
    }
    header = {
        "Host"   : "apserver.cloudtos.com",
        "Accept" : "application/json, text/plain, */*",
        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.50",
        "Content-Type" : "application/json; charset=UTF-8",
        "Origin" : "http://web.cloudtos.com",
        "Referer" : "http://web.cloudtos.com/",
        "Accept-Language" : "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    }
    req = RequestHandler()
    login_res = req.visit("post", url, json=Body)
    # login_text = login_res.text
    login_text = login_res.json()
    print(login_text['data']['Token'])

