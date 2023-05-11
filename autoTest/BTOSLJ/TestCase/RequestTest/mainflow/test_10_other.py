# -*- coding:utf-8 -*-
# Developer         : baishijun
# Development Time  : 2023/5/10 13:19
# Document Name     : test_02_daynightcount.PY
# Development Tool  : PyCharm
import datetime
import os
import allure
import pytest
from pytest_check import check
from BTOSLJ.Controls.BTOS_data import BtosCustomData
from BTOSLJ.PageObject.request_lj.num_validate_db import DataRes
from BTOSLJ.PageObject.request_lj.num_validate_interface import InterfaceRes
from config import host, header, db_host


@allure.epic('其他')
class TestOther:

    def setup_class(self):
        self.d = DataRes(db_host())
        self.r = InterfaceRes(host(), header())

    @allure.feature('计划管理')
    @allure.story('昼夜作业统计')
    @allure.title('吨位统计')
    def test_01_ton(self):
        plan_date = (datetime.date.today() + datetime.timedelta(days=-1)).strftime('%Y-%m-%d')
        actual_date = str(datetime.date.today())
        with allure.step("数据库请求"):
            expected_results = self.d.daynight_work_count_ton(plan_date, actual_date)
        with allure.step("接口请求"):
            actual_res = self.r.daynight_work_count_ton(plan_date, actual_date)
        with allure.step("数据比对"):
            expected_keys = [(data["日期"], data["工班"], data["计实"]) for data in expected_results]
            expected_indexs = {key: i for i, key in enumerate(expected_keys)}
            for data in actual_res["data"]:
                key = (data["timeType"], data["shiftCode"], data["planOrActual"])
                index = expected_indexs.get(key)
                check.is_not_none(index,
                                  "未匹配到数据: {}/{}/{}".format(data["timeType"], data["shiftCode"], data["planOrActual"]))
                if index is not None:
                    check.equal(float(data["ntrade"]), expected_results[index]["内贸"])
                    check.equal(float(data["wtrade"]), expected_results[index]["外贸"])
                    check.equal(float(data["barge"]), expected_results[index]["内河驳"])
                    check.equal(float(data["transit"]), expected_results[index]["中转"])
                    check.equal(float(data["delivery"]), expected_results[index]["进栈"])
                    check.equal(float(data["pickUp"]), expected_results[index]["出栈"])
                    check.equal(float(data["pickupDelivery"]), expected_results[index]["进出栈"])
                    check.equal(float(data["opTon"]), expected_results[index]["操作吨"])
                    check.equal(float(data["throughput"]), expected_results[index]["吞吐量"])

    @allure.feature('计划管理')
    @allure.story('昼夜作业统计')
    @allure.title('机械统计')
    def test_02_machine(self):
        actual_date = str(datetime.date.today())
        with allure.step("数据库请求"):
            expected_results = self.d.daynight_work_count_machine(actual_date)
        with allure.step("接口请求"):
            actual_res = self.r.daynight_work_count_machine(actual_date)
        with allure.step("数据比对"):
            expected_keys = [(data["名称"], data["代码"]) for data in expected_results]
            expected_indexs = {key: i for i, key in enumerate(expected_keys)}
            for data in actual_res["data"]:
                key = (data["stmMacTypeNm"], data["stmMacType"])
                index = expected_indexs.get(key)
                check.is_not_none(index, "未匹配到数据: {}/{}".format(data["stmMacTypeNm"], data["stmMacType"]))
                if index is not None:
                    check.equal(data["stmMacNumber"], expected_results[index]["数量"])

    def teardown_class(self):
        del self.d
        del self.r
