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
        schema = self.generate_schema(res, "1.json")
        check.equal(self.check_json(res, schema), True)

