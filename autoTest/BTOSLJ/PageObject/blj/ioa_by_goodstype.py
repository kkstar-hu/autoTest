# -*- coding:utf-8 -*-
from BTOSLJ.Controls.BTOS_requests import RequestMain
import pytest_check as check

class InterfaceRes(RequestMain):
    def test_ioabygoodstype_day(self, schema, workdata:str, ybkname:str):
        params = {
            "workdate": workdata,
            "termcd": "L",
            "ybkname": ybkname,
            "tenant_id": "SIPGLJ"
        }
        res = self.request_main("get","/api/blj/IOABYGOODSTYPE/DAY", params = params)
        data = res.json()
        check.equal(res.status_code, 200)
        check.equal(self.check_json(data, schema), True)
        self.logger.info("分货类进出存日报(IOABYGOODSTYPE/DAY)接口返回值\n参数: {}\n".format(params) + str(self.format(data)))


    def test_ioabygoodstype_month(self, schema, workdata:str, ybkname:str):
        params = {
            "workdate": workdata,
            "termcd": "L",
            "ybkname": ybkname,
            "tenant_id": "SIPGLJ"
        }
        res = self.request_main("get","/api/blj/IOABYGOODSTYPE/MONTH", params = params)
        data = res.json()
        check.equal(res.status_code, 200)
        check.equal(self.check_json(data, schema), True)
        self.logger.info("分货类进出存月报(IOABYGOODSTYPE/MONTH)接口返回值\n参数: {}\n".format(params) + str(self.format(data)))