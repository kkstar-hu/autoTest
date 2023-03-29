# -*- coding:utf-8 -*-
from BTOSLJ.Controls.BTOS_requests import RequestMain
import pytest_check as check

class IoaByGoodsTypeDay(RequestMain):
    def test_type(self, schema):
        params = {
            "workdate": "2023-03-24",
            "termcd": "L",
            "ybkname": "",
            "tenant_id": "SIPGLJ"
        }
        res = self.request_main("get","/api/blj/IOABYGOODSTYPE/DAY", params = params)
        data = res.json()
        check.equal(res.status_code, 200)
        check.equal(self.check_json(data, schema), True)


class IoaByGoodsTypeMonth(RequestMain):
    def test_type(self, schema):
        params = {
            "workdate": "2023-03-24",
            "termcd": "L",
            "ybkname": "",
            "tenant_id": "SIPGLJ"
        }
        res = self.request_main("get","/api/blj/IOABYGOODSTYPE/MONTH", params = params)
        data = res.json()
        check.equal(res.status_code, 200)
        check.equal(self.check_json(data, schema), True)