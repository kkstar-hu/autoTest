# -*- coding:utf-8 -*-
import json
from requests import exceptions
from BTOSLJ.Controls.BTOS_requests import RequestMain


def host():
    return "10.166.0.131:20000"


def header():
    return {
        'Content-Type': 'application/json',
        "Authorization": 'Bearer ' + get_token()
    }


def get_token():
    payload = {
        "little_girl": "ljadmin",
        "little_boy": "q1234567",
        "verification": "xxx"
    }
    headers = {'Content-Type': 'application/json'}
    r = RequestMain(host(), headers)
    try:
        res = r.request_main("POST", "/auth/saas/authorization/login/simple", headers=headers, json=payload)
    except exceptions.RequestException as e:
        r.logger.error("获取token失败", exc_info=True)
    else:
        return json.loads(res.text)["data"]["access_token"]
