# -*- coding:utf-8 -*-
# Developer         : baishijun
# Development Time  : 2023/5/10 13:48
# Document Name     : num_validate_interface.PY
# Development Tool  : PyCharm

from BTOSLJ.Controls.BTOS_requests import RequestMain
import pytest_check as check


class InterfaceRes(RequestMain):
    def daynight_work_count_ton(self, plan_date: str, actual_date: str):
        params = {
            "planDate": plan_date,
            "actualDate": actual_date,
            "termcd": 'L',
        }
        res = self.request_main("GET", "/tos/dts/report/dayAndNight/statistics", params=params)
        data = res.json()
        check.equal(res.status_code, 200)
        self.logger.info("计划管理-昼夜作业统计-吨位统计-接口返回值\n参数: {}\n".format(params) + str(self.format(data)))
        return data

    def daynight_work_count_machine(self, actual_date: str):
        params = {
            "opdate": actual_date
        }
        res = self.request_main("GET", "/tos/dts/shiftTaskMactype/machines/statistics", params=params)
        data = res.json()
        check.equal(res.status_code, 200)
        self.logger.info("计划管理-昼夜作业统计-机械出勤-接口返回值\n参数: {}\n".format(params) + str(self.format(data)))
        return data
