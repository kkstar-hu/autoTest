# -*- coding:utf-8 -*-
import allure
import pytest
from BTOSLJ.Controls.BTOS_requests import RequestMain
import pytest_check as check

class Blj(RequestMain):
    
    def test_type(self):
        params = {
            "workdate": "2023-03-24",
            "tenant_id": "SIPGLJ"
        }
        res = self.request_main("get","/api/blj/DAYNIGHTWORKHOUR/DAY", params = params)
        data = res.json()
        schema = self.load_json("workhour.json")
        check.equal(res.status_code, 200)
        check.equal(self.check_json(data, schema), True)

    def test_params_01(self):
        params = {
            "workdate": "2023-03-24"
        }
        res = self.request_main("get","/api/blj/DAYNIGHTWORKHOUR/DAY", params = params)
        data = res.json()
        schema = self.load_json("workhour.json")
        check.equal(res.status_code, 200)
        check.equal(self.check_json(data, schema), True)

    def test_params_02(self):
        params = {
            "tenant_id": "SIPGLJ"
        }
        res = self.request_main("get","/api/blj/DAYNIGHTWORKHOUR/DAY", params = params)
        data = res.json()
        schema = self.load_json("workhour.json")
        check.equal(res.status_code, 200)
        check.equal(self.check_json(data, schema), True)

    def test_no_params(self):
        params = {}
        res = self.request_main("get","/api/blj/DAYNIGHTWORKHOUR/DAY", params = params)
        data = res.json()
        schema = self.load_json("workhour.json")
        check.equal(res.status_code, 200)
        check.equal(self.check_json(data, schema), True)
        print(schema)

