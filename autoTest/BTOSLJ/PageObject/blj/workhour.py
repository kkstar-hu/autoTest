# -*- coding:utf-8 -*-
from BTOSLJ.Controls.BTOS_requests import RequestMain
import pytest_check as check

class WorkHour(RequestMain):
    
    def test_type(self, schema):
        params = {
            "workdate": "2023-03-24",
            "tenant_id": "SIPGLJ"
        }
        res = self.request_main("get","/api/blj/DAYNIGHTWORKHOUR/DAY", params = params)
        data = res.json()
        check.equal(res.status_code, 200)
        check.equal(self.check_json(data, schema), True)

    def test_params_01(self, schema):
        params = {
            "workdate": "2023-03-24"
        }
        res = self.request_main("get","/api/blj/DAYNIGHTWORKHOUR/DAY", params = params)
        data = res.json()
        check.equal(res.status_code, 200)
        check.equal(self.check_json(data, schema), True)

    def test_params_02(self, schema):
        params = {
            "tenant_id": "SIPGLJ"
        }
        res = self.request_main("get","/api/blj/DAYNIGHTWORKHOUR/DAY", params = params)
        data = res.json()
        check.equal(res.status_code, 200)
        check.equal(self.check_json(data, schema), True)

    def test_no_params(self, schema):
        params = {}
        res = self.request_main("get","/api/blj/DAYNIGHTWORKHOUR/DAY", params = params)
        data = res.json()
        check.equal(res.status_code, 200)
        check.equal(self.check_json(data, schema), True)


