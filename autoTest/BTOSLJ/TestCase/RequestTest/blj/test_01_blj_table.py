# -*- coding:utf-8 -*-
import os
import allure
import pytest
from BTOSLJ.PageObject.blj.workhour import WorkHour
from BTOSLJ.PageObject.blj.interface_res import InterfaceRes
from Commons.jsonread import read_json
from BTOSLJ.PageObject.blj.db_operate import DataRes


@allure.story('罗泾报表一期')
@allure.title('1.昼夜工时表')
@pytest.mark.parametrize("work_date",['2023-04-17'])
def test_workhuor(server_host, db_host, work_date):
    schema = read_json(os.path.join(os.getcwd(), r'schema\daynightworkhour.json'))
    with allure.step("接口请求"):
        r = InterfaceRes(server_host)
        r.test_daynightworkhour_day(schema, work_date)
    with allure.step("数据库请求"):
        d = DataRes(db_host)
        d.daynightworkhour_day(work_date)


@allure.story('罗泾报表一期')
@allure.title('2.分货类进出存日报表')
@pytest.mark.parametrize("work_date",['2023-04-17'])
def test_ioa_by_goodstype_day(server_host, db_host, work_date):
    schema = read_json(os.path.join(os.getcwd(), r'schema\ioabygoodstype_day.json'))
    with allure.step("接口请求"):
        r = InterfaceRes(server_host)
        r.test_ioabygoodstype_day(schema, work_date)
    with allure.step("数据库请求"):
        d = DataRes(db_host)
        d.ioabygoodstype_day(work_date)


@allure.story('罗泾报表一期')
@allure.title('3.分货类进出存月报表')
@pytest.mark.parametrize("work_date",['2023-04-17'])
def test_ioa_by_goodstype_month(server_host, db_host, work_date):
    schema = read_json(os.path.join(os.getcwd(), r'schema\ioabygoodstype_month.json'))
    with allure.step("接口请求"):
        r = InterfaceRes(server_host)
        r.test_ioabygoodstype_month(schema, work_date)
    with allure.step("数据库请求"):
        d = DataRes(db_host)
        d.ioabygoodstype_month(work_date)


@allure.story('罗泾报表一期')
@allure.title('4.内贸进口船舶作业情况统计表')
@pytest.mark.parametrize("starttm,endtm",[('2023-04-01','2023-04-17')])
def test_import_n(server_host, db_host, starttm, endtm):
    schema = read_json(os.path.join(os.getcwd(), r'schema\import_n.json'))
    with allure.step("接口请求"):
        r = InterfaceRes(server_host)
        r.test_import_n(schema, starttm, endtm)
    with allure.step("数据库请求"):
        d = DataRes(db_host)
        d.import_n(starttm, endtm)


@allure.story('罗泾报表一期')
@allure.title('5.外贸进口船舶作业情况统计表')
@pytest.mark.parametrize("starttm,endtm",[('2023-04-01','2023-04-17')])
def test_import_w(server_host, db_host,starttm, endtm):
    schema = read_json(os.path.join(os.getcwd(), r'schema\import_w.json'))
    with allure.step("接口请求"):
        r = InterfaceRes(server_host)
        r.test_import_w(schema, starttm, endtm)
    with allure.step("数据库请求"):
        d = DataRes(db_host)
        d.import_w(starttm, endtm)


@allure.story('罗泾报表一期')
@allure.title('6.外贸出口船舶作业情况统计表')
@pytest.mark.parametrize("starttm,endtm",[('2023-04-01','2023-04-17')])
def test_export_w(server_host, db_host,starttm, endtm):
    schema = read_json(os.path.join(os.getcwd(), r'schema\export_w.json'))
    with allure.step("接口请求"):
        r = InterfaceRes(server_host)
        r.test_export_w(schema, starttm, endtm)
    with allure.step("数据库请求"):
        d = DataRes(db_host)
        d.export_w(starttm, endtm)


@allure.story('罗泾报表一期')
@allure.title('7.分类定额效率统计表')
@pytest.mark.parametrize("start_date,end_date",[('2023-04-01','2023-04-17')])
def test_quona_workpiece_ratio_count(server_host, db_host, start_date, end_date):
    schema = read_json(os.path.join(os.getcwd(), r'schema\quona_workpiece_ratio_count.json'))
    with allure.step("接口请求"):
        r = InterfaceRes(server_host)
        r.test_quona_workpiece_ratio_count(schema, start_date, end_date)
    with allure.step("数据库请求"):
        d = DataRes(db_host)
        d.quona_workpiece_ratio_count(start_date, end_date)


@allure.story('罗泾报表一期')
@allure.title('8.保税仓库库场情况表')
def test_bondedcase_day(server_host, db_host):
    schema = read_json(os.path.join(os.getcwd(), r'schema\bondedcase_day.json'))
    with allure.step("接口请求"):
        r = InterfaceRes(server_host)
        r.test_bondedcase_day(schema)
    with allure.step("数据库请求"):
        d = DataRes(db_host)
        d.bondedcase_day()


@allure.story('罗泾报表一期')
@allure.title('9.保税仓库进出报表')
@pytest.mark.parametrize("start_date,end_date,bod_no,billNbr,vslname",
                         [('2023-04-01','2023-04-17','2',"CD20230410LJ004","丽萨")])
def test_bondedio_day(server_host, db_host,start_date,end_date,bod_no,billNbr,vslname):
    schema = read_json(os.path.join(os.getcwd(), r'schema\bondedio_day.json'))
    with allure.step("接口请求"):
        r = InterfaceRes(server_host)
        r.test_bondedio_day(schema, start_date, end_date, bod_no, billNbr, vslname)
    with allure.step("数据库请求"):
        d = DataRes(db_host)
        d.bondedio_day(start_date, end_date, bod_no, billNbr, vslname)


@allure.story('罗泾报表一期')
@allure.title('10.船舶工时表')
@pytest.mark.parametrize("start_date,end_date,pws_voy_id,route_sign",
                         [('2023-04-01','2023-04-17','6f3683616ec7f2a09087b634352a6538','00018010')])
def test_shipworkhour(server_host, db_host,start_date,end_date,pws_voy_id,route_sign):
    schema = read_json(os.path.join(os.getcwd(), r'schema\shipworkhour.json'))
    with allure.step("接口请求"):
        r = InterfaceRes(server_host)
        r.test_shipworkhour(schema, start_date, end_date, pws_voy_id, route_sign)
    with allure.step("数据库请求"):
        d = DataRes(db_host)
        d.shipworkhour_wk(start_date, end_date, pws_voy_id, route_sign)
        d.shipworkhour_machine(start_date, end_date, pws_voy_id, route_sign)


@allure.story('罗泾报表一期')
@allure.title('11.昼夜作业情况统计表')
@pytest.mark.parametrize("work_date",['2023-04-17'])
def test_daynightworksta_day(server_host, db_host,work_date):
    schema = read_json(os.path.join(os.getcwd(), r'schema\daynightworksta_day.json'))
    with allure.step("接口请求"):
        r = InterfaceRes(server_host)
        r.test_daynightworksta_day(schema, work_date)
    with allure.step("数据库请求"):
        d = DataRes(db_host)
        d.daynightworksta_day(work_date)
        d.daynightworksta_zj(work_date)
        d.daynightworksta_store(work_date)
        d.daynightworksta_paper(work_date)
        d.daynightworksta_nin(work_date)
