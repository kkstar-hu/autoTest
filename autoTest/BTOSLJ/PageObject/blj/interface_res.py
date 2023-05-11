# -*- coding:utf-8 -*-
from BTOSLJ.Controls.BTOS_requests import RequestMain
import pytest_check as check


class InterfaceRes(RequestMain):
    def test_ioabygoodstype_day(self, schema, workdata: str, ybkname="全部"):
        params = {
            "workdate": workdata,
            "termcd": "L",
            "ybkname": ybkname,
            "tenant_id": "SIPGLJ"
        }
        res = self.request_main("get", "/api/blj/IOABYGOODSTYPE/DAY", params=params)
        data = res.json()
        check.equal(res.status_code, 200)
        check.equal(self.check_json(data, schema), True)
        self.logger.info("分货类进出存日报(IOABYGOODSTYPE/DAY)-接口返回值\n参数: {}\n".format(params) + str(self.format(data)))

    def test_ioabygoodstype_month(self, schema, workdata: str, ybkname="全部"):
        params = {
            "workdate": workdata,
            "termcd": "L",
            "ybkname": ybkname,
            "tenant_id": "SIPGLJ"
        }
        res = self.request_main("get", "/api/blj/IOABYGOODSTYPE/MONTH", params=params)
        data = res.json()
        check.equal(res.status_code, 200)
        check.equal(self.check_json(data, schema), True)
        self.logger.info("分货类进出存月报(IOABYGOODSTYPE/MONTH)-接口返回值\n参数: {}\n".format(params) + str(self.format(data)))

    def test_daynightworkhour_day(self, schema, work_date):
        params = {
            "workdate": work_date,
            "tenant_id": "SIPGLJ"
        }
        res = self.request_main("get", "/api/blj/DAYNIGHTWORKHOUR/DAY", params=params)
        data = res.json()
        check.equal(res.status_code, 200)
        check.equal(self.check_json(data, schema), True)
        self.logger.info("昼夜工时表(DAYNIGHTWORKHOUR/DAY)-接口返回值\n参数: {}\n".format(params) + str(self.format(data)))
        return data

    def test_import_n(self, schema, starttm: str, endtm: str):
        params = {
            "STARTTM": starttm,
            "ENDTM": endtm
        }
        res = self.request_main("get", "/api/blj/import_N", params=params)
        data = res.json()
        check.equal(res.status_code, 200)
        check.equal(self.check_json(data, schema), True)
        self.logger.info("内贸进口船舶作业情况统计(import_N)-接口返回值\n参数: {}\n".format(params) + str(self.format(data)))
        return data

    def test_import_w(self, schema, starttm: str, endtm: str):
        params = {
            "STARTTM": starttm,
            "ENDTM": endtm
        }
        res = self.request_main("get", "/api/blj/import_W", params=params)
        data = res.json()
        check.equal(res.status_code, 200)
        check.equal(self.check_json(data, schema), True)
        self.logger.info("外贸进口船舶作业情况统计(import_W)-接口返回值\n参数: {}\n".format(params) + str(self.format(data)))
        return data

    def test_export_w(self, schema, starttm: str, endtm: str):
        params = {
            "STARTTM": starttm,
            "ENDTM": endtm
        }
        res = self.request_main("get", "/api/blj/export_W", params=params)
        data = res.json()
        check.equal(res.status_code, 200)
        check.equal(self.check_json(data, schema), True)
        self.logger.info("外贸出口船舶作业情况统计(export_W)-接口返回值\n参数: {}\n".format(params) + str(self.format(data)))
        return data

    def test_quona_workpiece_ratio_count(self, schema, start_date: str, end_date: str):
        params = {
            "startdate": start_date,
            "enddate": end_date,
            "tenant_id": 'SIPGLJ'
        }
        res = self.request_main("get", "/api/blj/quona_workpiece_ratio_count/day", params=params)
        data = res.json()
        check.equal(res.status_code, 200)
        check.equal(self.check_json(data, schema), True)
        self.logger.info(
            "分类定额效率统计(quona_workpiece_ratio_count/day)-接口返回值\n参数: {}\n".format(params) + str(self.format(data)))
        return data

    def test_bondedcase_day(self, schema):
        params = {
            "tenant_id": 'SIPGLJ'
        }
        res = self.request_main("get", "/api/blj/BONDEDCASE/DAY")
        data = res.json()
        check.equal(res.status_code, 200)
        check.equal(self.check_json(data, schema), True)
        self.logger.info("保税仓库库场情况(BONDEDCASE/DAY)-接口返回值\n参数: {}\n".format(params) + str(self.format(data)))
        return data

    def test_bondedio_day(self, schema, start_date, end_date, bod_no=None, billNbr=None, vslname=None):
        params = {
            "startdate": start_date,
            "enddate": end_date,
            "bod_no": bod_no,
            "billNbr": billNbr,
            "vslname": vslname,
            "tenant_id": 'SIPGLJ'
        }
        res = self.request_main("get", "/api/blj/BONDEDIO/DAY", params=params)
        data = res.json()
        check.equal(res.status_code, 200)
        check.equal(self.check_json(data, schema), True)
        self.logger.info("保税仓库进出报表(BONDEDIO/DAY)-接口返回值\n参数: {}\n".format(params) + str(self.format(data)))
        return data

    def test_shipworkhour(self, schema, start_date, end_date, pws_voy_id, route_sign=None):
        params = {
            "startdate": start_date,
            "enddate": end_date,
            "pws_voy_id": pws_voy_id,
            "route_sign": route_sign,
            "tenant_id": 'SIPGLJ'
        }
        res = self.request_main("get", "/api/blj/SHIPWORKHOUR/DAY", params=params)
        data = res.json()
        check.equal(res.status_code, 200)
        check.equal(self.check_json(data, schema), True)
        self.logger.info("船舶工时表(SHIPWORKHOUR/DAY)-接口返回值\n参数: {}\n".format(params) + str(self.format(data)))
        return data


    def test_daynightworksta_day(self, schema, work_date: str):
        params = {
            "workdate": work_date,
            "tenant_id": "SIPGLJ"
        }
        res = self.request_main("get", "/api/blj/DAYNIGHTWORKSTA/DAY", params=params)
        data = res.json()
        check.equal(res.status_code, 200)
        check.equal(self.check_json(data, schema), True)
        self.logger.info("昼夜作业情况统计表(DAYNIGHTWORKSTA/DAY)-接口返回值\n参数: {}\n".format(params) + str(self.format(data)))
        return data


    def test_vagt_wgood(self, schema, yyyy: str, mm: str):
        params = {
            "yyyy": yyyy,
            "tenant_id": "SIPGLJ",
            "mm": mm
        }
        res = self.request_main("get", "/api/VAGT/WGOOD", params=params)
        data = res.json()
        check.equal(res.status_code, 200)
        check.equal(self.check_json(data, schema), True)
        self.logger.info("船代外贸进出口(VAGT/WGOOD)-接口返回值\n参数: {}\n".format(params) + str(self.format(data)))
        return data


    def test_voyage_count(self, schema, yyyy: str):
        params = {
            "yyyy": yyyy,
            "tenant_id": "SIPGLJ"
        }
        res = self.request_main("get", "/api/voyage/count", params=params)
        data = res.json()
        check.equal(res.status_code, 200)
        check.equal(self.check_json(data, schema), True)
        self.logger.info("航线统计表(voyage/count)-接口返回值\n参数: {}\n".format(params) + str(self.format(data)))


    def test_boatcompany_day(self, schema, work_date: str):
        params = {
            "workdate": work_date,
            "tenant_id": "SIPGLJ"
        }
        res = self.request_main("get", "/api/blj/BOATCOMPANY/DAY", params=params)
        data = res.json()
        check.equal(res.status_code, 200)
        check.equal(self.check_json(data, schema), True)
        self.logger.info("船公司外贸进出口(BOATCOMPANY/DAY)-接口返回值\n参数: {}\n".format(params) + str(self.format(data)))
        return data


    def test_maingoods_dclddtl(self, schema, yyyy: str):
        params = {
            "yyyy": yyyy,
            "tenant_id": "SIPGLJ"
        }
        res = self.request_main("get", "/api/MAINGOODS/DCLDDTL", params=params)
        data = res.json()
        check.equal(res.status_code, 200)
        check.equal(self.check_json(data, schema), True)
        self.logger.info("主要货种完成量(MAINGOODS/DCLDDTL)-接口返回值\n参数: {}\n".format(params) + str(self.format(data)))
