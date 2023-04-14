# -*- coding:utf-8 -*-
import time
from BTOSLJ.Controls.BTOS_db import GetPg
import uuid
import pandas as pd

class DataRes(GetPg):


    def import_n(self, starttm:str, endtm:str):
        sql = self.load_sql("sql/import_N.sql")\
            .format(starttm = starttm, endtm = endtm)
        res = self.select_from_table(sql)
        self.logger.info('内贸进口船舶作业情况统计(import_N)-sql结果\n参数: starttm = {}, endtm = {}\n'
                         .format(starttm,endtm) + self.to_json(res))


    def import_w(self, starttm:str, endtm:str):
        sql = self.load_sql("sql/import_W.sql")\
            .format(starttm = starttm, endtm = endtm)
        res = self.select_from_table(sql)
        self.logger.info('外贸进口船舶作业情况统计(import_W)-sql结果\n参数: starttm = {}, endtm = {}\n'
                         .format(starttm,endtm) + self.to_json(res))


    def export_w(self, starttm:str, endtm:str):
        sql = self.load_sql("sql/export_W.sql")\
            .format(starttm = starttm, endtm = endtm)
        res = self.select_from_table(sql)
        self.logger.info('外贸进口船舶作业情况统计(export_W)-sql结果\n参数: starttm = {}, endtm = {}\n'
                         .format(starttm,endtm) + self.to_json(res))


    def quona_workpiece_ratio_count(self, start_date:str, end_date:str):
        sql = self.load_sql("sql/quona_workpiece_ratio_count.sql")\
            .format(start_date = start_date,end_date = end_date)
        res = self.select_from_table(sql)
        self.logger.info('分类效率统计(quona_workpiece_ratio_count)-sql结果\n参数: start_date = {}, end_date = {}\n'
                         .format(start_date,end_date) + self.to_json(res))

    def ioabygoodstype_day(self, work_date:str, ybk_name="全部"):
        sql = self.load_sql("sql/ioabygoodstype_day.sql")\
            .format(workdate = work_date,ybkname = ybk_name)
        res = self.select_from_table(sql)
        self.logger.info('分货类进出存日报(ioabygoodstype_day)-sql结果\n参数: work_date = {}, ybk_name = {}\n'
                         .format(work_date, ybk_name) + self.to_json(res))

    def ioabygoodstype_month(self, work_date:str, ybk_name="全部"):
        sql = self.load_sql("sql/ioabygoodstype_month.sql")\
            .format(workdate = work_date,ybkname = ybk_name)
        res = self.select_from_table(sql)
        self.logger.info('分货类进出存月报(ioabygoodstype_month)-sql结果\n参数: work_date = {}, ybk_name = {}\n'
                         .format(work_date, ybk_name) + self.to_json(res))


    def bondedcase_day(self):
        sql = self.load_sql("sql/bondedcase_day.sql")
        res = self.select_from_table(sql)
        self.logger.info('保税仓库库场情况(bondedcase_day)-sql结果\n参数: 无\n' + self.to_json(res))


    def bondedio_day(self, start_date, end_date):
        sql = self.load_sql("sql/bondedio_day.sql")\
            .format(startdate = start_date, enddate = end_date)
        res = self.select_from_table(sql)
        self.logger.info('保税仓库进出报表(bondedio_day)-sql结果\n参数: start_date = {}, end_date = {}\n'
                         .format(start_date, end_date) + self.to_json(res))


    def shipworkhour_wk(self):
        sql = self.load_sql("sql/shipworkhour_wk.sql")
        res = self.select_from_table(sql)
        self.logger.info('船舶工时表_装卸队(shipworkhour_wk)-sql结果\n参数: 无\n' + self.to_json(res))


    def shipworkhour_machine(self):
        sql = self.load_sql("sql/shipworkhour_machine.sql")
        res = self.select_from_table(sql)
        self.logger.info('船舶工时表_员工(shipworkhour_machine)-sql结果\n参数: 无\n' + self.to_json(res))


    def daynightworkhour_day(self):
        sql = self.load_sql("sql/daynightworkhour_day.sql")
        res = self.select_from_table(sql)
        self.logger.info('昼夜工时表(daynightworkhour_day)-sql结果\n参数: 无\n' + self.to_json(res))

if __name__ == "__main__":
    a = DataRes("10.116.8.20")
    #a.quona_workpiece_ratio_count('2023-01-01','2023-04-14')
    #a.import_n('2023-01-01','2023-04-14')
    #a.import_w('2023-01-01','2023-04-14')
    #a.export_w('2023-01-01','2023-04-14')
    #a.ioabygoodstype_day('2023-04-14')
    #a.ioabygoodstype_month('2023-04-14')
    #a.bondedcase_day()
    #a.bondedcase_day('2023-01-01','2023-04-14')
    #a.shipworkhour_wk()
    #a.shipworkhour_machine()
    a.daynightworkhour_day()

