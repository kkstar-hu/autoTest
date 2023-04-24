# -*- coding:utf-8 -*-
import os
import time
from BTOSLJ.Controls.BTOS_db import GetPg
import uuid
import pandas as pd


class DataRes(GetPg):

    def import_n(self, starttm: str, endtm: str):
        sql = self.load_sql(os.path.join(os.path.dirname(__file__), r"sql\import_N.sql")) \
            .format(starttm=starttm, endtm=endtm)
        res = self.select_from_table(sql)
        self.logger.info('内贸进口船舶作业情况统计(import_N)-sql结果\n参数: starttm = {}, endtm = {}\n'
                         .format(starttm, endtm) + self.to_json(res))
        return self.to_json_dict(res)


    def import_w(self, starttm: str, endtm: str):
        sql = self.load_sql(os.path.join(os.path.dirname(__file__), r"sql\import_W.sql")) \
            .format(starttm=starttm, endtm=endtm)
        res = self.select_from_table(sql)
        self.logger.info('外贸进口船舶作业情况统计(import_W)-sql结果\n参数: starttm = {}, endtm = {}\n'
                         .format(starttm, endtm) + self.to_json(res))
        return self.to_json_dict(res)


    def export_w(self, starttm: str, endtm: str):
        sql = self.load_sql(os.path.join(os.path.dirname(__file__), r"sql\export_W.sql")) \
            .format(starttm=starttm, endtm=endtm)
        res = self.select_from_table(sql)
        self.logger.info('外贸出口船舶作业情况统计(export_W)-sql结果\n参数: starttm = {}, endtm = {}\n'
                         .format(starttm, endtm) + self.to_json(res))
        return self.to_json_dict(res)


    def quona_workpiece_ratio_count(self, start_date: str, end_date: str):
        sql = self.load_sql(os.path.join(os.path.dirname(__file__), r"sql\quona_workpiece_ratio_count.sql")) \
            .format(start_date=start_date, end_date=end_date)
        res = self.select_from_table(sql)
        self.logger.info('分类定额效率统计(quona_workpiece_ratio_count)-sql结果\n参数: start_date = {}, end_date = {}\n'
                         .format(start_date, end_date) + self.to_json(res))
        return self.to_json_dict(res)


    def ioabygoodstype_day(self, work_date: str, ybk_name="全部"):
        sql = self.load_sql(os.path.join(os.path.dirname(__file__), r"sql\ioabygoodstype_day.sql")) \
            .format(workdate=work_date, ybkname=ybk_name)
        res = self.select_from_table(sql)
        self.logger.info('分货类进出存日报(ioabygoodstype_day)-sql结果\n参数: work_date = {}, ybk_name = {}\n'
                         .format(work_date, ybk_name) + self.to_json(res))


    def ioabygoodstype_month(self, work_date: str, ybk_name="全部"):
        sql = self.load_sql(os.path.join(os.path.dirname(__file__), r"sql\ioabygoodstype_month.sql")) \
            .format(workdate=work_date, ybkname=ybk_name)
        res = self.select_from_table(sql)
        self.logger.info('分货类进出存月报(ioabygoodstype_month)-sql结果\n参数: work_date = {}, ybk_name = {}\n'
                         .format(work_date, ybk_name) + self.to_json(res))


    def bondedcase_day(self):
        sql = self.load_sql(os.path.join(os.path.dirname(__file__), r"sql\bondedcase_day.sql"))
        res = self.select_from_table(sql)
        self.logger.info('保税仓库库场情况(bondedcase_day)-sql结果\n参数: 无\n' + self.to_json(res))
        return self.to_json_dict(res)


    def bondedio_day(self, start_date, end_date, bod_no=None, billNbr=None, vslname=None):
        bod_no1 = "and res.料号='" + bod_no + "'" if bod_no != None else ""
        billNbr1 = "and res.提单号='" + billNbr + "'" if billNbr != None else ""
        vslname1 = "and res.船名='" + vslname + "'" if vslname != None else ""
        sql = self.load_sql(os.path.join(os.path.dirname(__file__), r"sql\bondedio_day.sql")) \
            .format(startdate=start_date, enddate=end_date, bod_no=bod_no1, billNbr=billNbr1, vslname=vslname1)
        res = self.select_from_table(sql)
        self.logger.info('保税仓库进出报表(bondedio_day)-sql结果\n参数: start_date = {}, end_date = {}, bod_no={}, billNbr={}, '
                         'vslname={}\n'.format(start_date, end_date, bod_no, billNbr, vslname) + self.to_json(res))
        return self.to_json_dict(res)


    def shipworkhour_wk(self, start_date, end_date, pws_voy_id, route_sign=None):
        route_sign1 = "and wsw.wsw_route_sign='" + route_sign + "'" if route_sign != None else ""
        sql = self.load_sql(os.path.join(os.path.dirname(__file__), r"sql\shipworkhour_wk.sql")) \
            .format(startdate=start_date, enddate=end_date, pws_voy_id=pws_voy_id, route_sign=route_sign1)
        res = self.select_from_table(sql)
        self.logger.info('船舶工时表_装卸队(shipworkhour_wk)-sql结果\n参数: start_date = {}, end_date = {}, pws_voy_id={}, '
                         'route_sign={}\n'.format(start_date, end_date, pws_voy_id, route_sign) + self.to_json(res))


    def shipworkhour_machine(self, start_date, end_date, pws_voy_id, route_sign=None):
        route_sign1 = "and wsm.wsm_route_sign='" + route_sign + "'" if route_sign != None else ""
        sql = self.load_sql(os.path.join(os.path.dirname(__file__), r"sql\shipworkhour_machine.sql")) \
            .format(startdate=start_date, enddate=end_date, pws_voy_id=pws_voy_id, route_sign=route_sign1)
        res = self.select_from_table(sql)
        self.logger.info('船舶工时表_员工(shipworkhour_machine)-sql结果\n参数: start_date = {}, end_date = {}, pws_voy_id={}, '
                         'route_sign={}\n'.format(start_date, end_date, pws_voy_id, route_sign) + self.to_json(res))
        return self.to_json_dict(res)


    def daynightworkhour_day(self, work_date: str):
        sql = self.load_sql(os.path.join(os.path.dirname(__file__), r"sql\daynightworkhour_day.sql")).format(
            workdate=work_date)
        res = self.select_from_table(sql)
        self.logger.info('昼夜工时表(daynightworkhour_day)-sql结果\n参数: workdate = {}\n'.format(work_date) + self.to_json(res))
        return self.to_json_dict(res)


    def daynightworksta_day(self, work_date: str):
        sql = self.load_sql(os.path.join(os.path.dirname(__file__), r"sql\daynightworksta_day.sql")).format(
            workdate=work_date)
        res = self.select_from_table(sql)
        self.logger.info(
            '昼夜作业情况统计表-分货类结存(daynightworksta)-sql结果\n参数: work_date = {}\n'.format(work_date) + self.to_json(res))
        return self.to_json_dict(res)


    def daynightworksta_store(self, work_date: str):
        sql = self.load_sql(os.path.join(os.path.dirname(__file__), r"sql\daynightworksta_store.sql")).format(
            workdate=work_date)
        res = self.select_from_table(sql)
        self.logger.info(
            '昼夜作业情况统计表-堆存情况(daynightworksta)-sql结果\n参数: work_date = {}\n'.format(work_date) + self.to_json(res))
        return self.to_json_dict(res)


    def daynightworksta_zj(self, work_date: str):
        sql = self.load_sql(os.path.join(os.path.dirname(__file__), r"sql\daynightworksta_zj.sql")).format(
            workdate=work_date)
        res = self.select_from_table(sql)
        self.logger.info(
            '昼夜作业情况统计表-桩脚(daynightworksta)-sql结果\n参数: work_date = {}\n'.format(work_date) + self.to_json(res))
        return self.to_json_dict(res)


    def daynightworksta_paper(self, work_date: str):
        sql = self.load_sql(os.path.join(os.path.dirname(__file__), r"sql\daynightworksta_paper.sql")).format(
            workdate=work_date)
        res = self.select_from_table(sql)
        self.logger.info(
            '昼夜作业情况统计表-本日纸浆提货情况(daynightworksta)-sql结果\n参数: work_date = {}\n'.format(work_date) + self.to_json(res))
        return self.to_json_dict(res)


    def daynightworksta_nin(self, work_date: str):
        sql = self.load_sql(os.path.join(os.path.dirname(__file__), r"sql\daynightworksta_nin.sql")).format(
            workdate=work_date)
        res = self.select_from_table(sql)
        self.logger.info(
            '昼夜作业情况统计表-本日内贸进场情况(daynightworksta)-sql结果\n参数: work_date = {}\n'.format(work_date) + self.to_json(res))
        return self.to_json_dict(res)


    def vagt_wgood(self, yyyy: str, mm: str):
        sql = self.load_sql(os.path.join(os.path.dirname(__file__), r"sql\vagt_wgood.sql")).format(
            workdate=yyyy + '-' + mm)
        res = self.select_from_table(sql)
        self.logger.info('船代外贸进出口(vagt_wgood)-sql结果\n参数: yyyy = {}, mm = {}\n'
                         .format(yyyy, mm) + self.to_json(res))
        return self.to_json_dict(res)


    def voyage_count(self, yyyy: str):
        sql = self.load_sql(os.path.join(os.path.dirname(__file__), r"sql\voyage_count.sql"))\
            .format(yyyy1=yyyy, yyyy2=int(yyyy) - 1)
        res = self.select_from_table(sql)
        self.logger.info('航线统计表(voyage_count)-sql结果\n参数: yyyy = {}\n'
                         .format(yyyy) + self.to_json(res))


    def boatcompany_day(self, work_date: str):
        sql = self.load_sql(os.path.join(os.path.dirname(__file__), r"sql\boatcompany_day.sql")).format(
            workdate=work_date)
        res = self.select_from_table(sql)
        self.logger.info('船公司外贸进出口(boatcompany_day)-sql结果\n参数: workdate = {}\n'
                         .format(work_date) + self.to_json(res))
        return self.to_json_dict(res)


    def maingoods_dclddtl(self, yyyy: str):
        sql = self.load_sql(os.path.join(os.path.dirname(__file__), r"sql\maingoods_dclddtl.sql"))\
            .format(yyyy1=yyyy, yyyy2=int(yyyy) - 1)
        res = self.select_from_table(sql)
        self.logger.info('主要货种完成量(maingoods_dclddtl)-sql结果\n参数: yyyy = {}\n'
                         .format(yyyy) + self.to_json(res))


if __name__ == "__main__":
    a = DataRes("10.116.8.20")
    # a.quona_workpiece_ratio_count('2023-01-01','2023-04-14')
    # a.import_n('2023-01-01','2023-04-14')
    # a.import_w('2023-01-01','2023-04-14')
    # a.export_w('2023-01-01','2023-04-14')
    # a.ioabygoodstype_day('2023-04-14')
    # a.ioabygoodstype_month('2023-04-14')
    # a.bondedcase_day()
    # a.bondedio_day('2023-01-01','2023-04-14',bod_no="2",billNbr="CD20230410LJ004",vslname="丽萨")
    # a.shipworkhour_wk('2023-01-01','2023-04-17','6f3683616ec7f2a09087b634352a6538','00018010')
    # a.shipworkhour_machine('2023-01-01','2023-04-17','6f3683616ec7f2a09087b634352a6538','00018010')
    # a.daynightworkhour_day('2023-04-10')
    # a.daynightworksta_day('2023-04-10')
    # a.daynightworksta_store('2023-04-10')
    # a.daynightworksta_zj('2023-04-17')
    # a.daynightworksta_paper('2023-04-11')
    # a.daynightworksta_nin('2023-04-14')
    # a.vagt_wgood('2023','04')
    # a.voyage_count('2023')
    # a.boatcompany_day('2023-04-20')
    # a.maingoods_dclddtl('2023')
