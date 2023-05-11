# -*- coding:utf-8 -*-
# Developer         : baishijun
# Development Time  : 2023/5/10 13:20
# Document Name     : day_night_work_count.PY
# Development Tool  : PyCharm

import os
from BTOSLJ.Controls.BTOS_db import GetPg


class DataRes(GetPg):
    def daynight_work_count_ton(self, plan_date: str, actual_date: str):
        sql = self.load_sql(os.path.join(os.path.dirname(__file__), r"sql/daynight_work_count_ton.sql")) \
            .format(plan_date=plan_date, actual_date=actual_date)
        res = self.select_from_table(sql)
        self.logger.info('计划管理-昼夜作业统计-吨位统计(import_N)-sql结果\n参数: plan_date = {}, actual_date = {}\n'
                         .format(plan_date, actual_date) + self.to_json(res))
        return self.to_json_dict(res)

    def daynight_work_count_machine(self, actual_date: str):
        sql = self.load_sql(os.path.join(os.path.dirname(__file__), r"sql/daynight_work_count_machine.sql")) \
            .format(actual_date=actual_date)
        res = self.select_from_table(sql)
        self.logger.info('计划管理-昼夜作业统计-机械统计(import_N)-sql结果\n参数: actual_date = {}\n'
                         .format(actual_date) + self.to_json(res))
        return self.to_json_dict(res)


