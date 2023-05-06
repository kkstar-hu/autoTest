# -*- coding:utf-8 -*-
import os
import allure
import pytest
from pytest_check import check
from BTOSLJ.PageObject.blj.workhour import WorkHour
from BTOSLJ.PageObject.blj.interface_res import InterfaceRes
from Commons.jsonread import read_json
from BTOSLJ.PageObject.blj.db_operate import DataRes


@allure.story('罗泾报表一期')
@allure.title('1.昼夜工时表')
@pytest.mark.parametrize("work_date", ['2023-04-17'])
def test_daynightworkhour_day(server_host, db_host, work_date):
    schema = read_json(os.path.join(os.getcwd(), r'schema\daynightworkhour.json'))
    with allure.step("接口请求"):
        r = InterfaceRes(server_host)
        res = r.test_daynightworkhour_day(schema, work_date)
    with allure.step("数据库请求"):
        d = DataRes(db_host)
        expected_results = d.daynightworkhour_day(work_date)
    with allure.step("数据比对"):
        expected_keys = [(data["组别"], data["时间"]) for data in expected_results]
        expected_indexs = {key: i for i, key in enumerate(expected_keys)}
        for data in res["data"]:
            key = (data["name"], data["type"])
            index = expected_indexs.get(key)
            # check.is_not_none(index, "接口响应结果中缺少name={},type={}的数据".format(data["组别"], data["时间"]))
            if index is not None:
                check.equal(data["shwg"], expected_results[index]["大船吨位"])
                check.equal(data["shhour"], expected_results[index]["大船工时"])
                check.equal(data["nwg"], expected_results[index]["内贸吨位"])
                check.equal(data["nhour"], expected_results[index]["内贸工时"])
                check.equal(data["wwg"], expected_results[index]["外贸吨位"])
                check.equal(data["whour"], expected_results[index]["外贸工时"])
                check.equal(data["bwg"], expected_results[index]["内河驳吨位"])
                check.equal(data["bhour"], expected_results[index]["内河驳工时"])
                check.equal(data["ywg"], expected_results[index]["进出栈吨位"])
                check.equal(data["yhour"], expected_results[index]["进出栈工时"])
                check.equal(data["zwg"], expected_results[index]["杂项吨位"])
                check.equal(data["zhour"], expected_results[index]["杂项工时"])


@allure.story('罗泾报表一期')
@allure.title('2.分货类进出存日报表')
@pytest.mark.parametrize("work_date", ['2023-04-17'])
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
@pytest.mark.parametrize("work_date", ['2023-04-17'])
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
@pytest.mark.parametrize("starttm,endtm", [('2023-04-01', '2023-04-17')])
def test_import_n(server_host, db_host, starttm, endtm):
    schema = read_json(os.path.join(os.getcwd(), r'schema\import_n.json'))
    with allure.step("接口请求"):
        r = InterfaceRes(server_host)
        res = r.test_import_n(schema, starttm, endtm)
    with allure.step("数据库请求"):
        d = DataRes(db_host)
        expected_results = d.import_n(starttm, endtm)
    with allure.step("数据比对"):
        expected_keys = [(data["船名"], data["航次"]) for data in expected_results]
        expected_indexs = {key: i for i, key in enumerate(expected_keys)}
        check.equal(len(expected_results)-1, len(res["data"]), "数据量不相等")
        for data in res["data"]:
            key = (data["vsl_cnname"], data["voy_voyage"])
            index = expected_indexs.get(key)
            check.is_not_none(index, "未匹配到数据: {}/{}".format(data["vsl_cnname"], data["voy_voyage"]))
            if index is not None:
                check.equal(data["bil_gtpks_total"], expected_results[index]["舱单件数"])
                check.equal(data["bil_gtwg_total"], expected_results[index]["舱单重量"])
                check.equal(data["vt_goa_gtpks"], expected_results[index]["车直提件数"])
                check.equal(data["vt_goa_gtwg"], expected_results[index]["车直提重量"])
                check.equal(data["vb_goa_gtpks"], expected_results[index]["驳直提件数"])
                check.equal(data["vb_goa_gtwg"], expected_results[index]["驳直提重量"])
                check.equal(data["vy_goa_gtpks"], expected_results[index]["进场件数"])
                check.equal(data["vy_goa_gtwg"], expected_results[index]["进场重量"])
                check.equal(data["yt_goa_gtpks"], expected_results[index]["库场提货件数"])
                check.equal(data["yt_goa_gtwg"], expected_results[index]["库场提货重量"])
                check.equal(data["IN_YARD_GTPKS"], expected_results[index]["剩余件数"])
                check.equal(data["IN_YARD_GTWG"], expected_results[index]["剩余重量"])


@allure.story('罗泾报表一期')
@allure.title('5.外贸进口船舶作业情况统计表')
@pytest.mark.parametrize("starttm,endtm", [('2023-04-01', '2023-04-17')])
def test_import_w(server_host, db_host, starttm, endtm):
    schema = read_json(os.path.join(os.getcwd(), r'schema\import_w.json'))
    with allure.step("接口请求"):
        r = InterfaceRes(server_host)
        res = r.test_import_w(schema, starttm, endtm)
    with allure.step("数据库请求"):
        d = DataRes(db_host)
        expected_results = d.import_w(starttm, endtm)
    with allure.step("数据比对"):
        expected_keys = [(data["船名"], data["航次"]) for data in expected_results]
        expected_indexs = {key: i for i, key in enumerate(expected_keys)}
        check.equal(len(expected_results)-1, len(res["data"]), "数据量不相等")
        for data in res["data"]:
            key = (data["vsl_cnname"], data["voy_voyage"])
            index = expected_indexs.get(key)
            check.is_not_none(index, "未匹配到数据: {}/{}".format(data["vsl_cnname"], data["voy_voyage"]))
            if index is not None:
                check.equal(data["bil_gtpks_total"], expected_results[index]["舱单件数"])
                check.equal(data["bil_gtwg_total"], expected_results[index]["舱单重量"])
                check.equal(data["vt_goa_gtpks"], expected_results[index]["车直提件数"])
                check.equal(data["vt_goa_gtwg"], expected_results[index]["车直提重量"])
                check.equal(data["vb_goa_gtpks"], expected_results[index]["驳直提件数"])
                check.equal(data["vb_goa_gtwg"], expected_results[index]["驳直提重量"])
                check.equal(data["vy_goa_gtpks"], expected_results[index]["进场件数"])
                check.equal(data["vy_goa_gtwg"], expected_results[index]["进场重量"])
                check.equal(data["yt_goa_gtpks"], expected_results[index]["库场提货件数"])
                check.equal(data["yt_goa_gtwg"], expected_results[index]["库场提货重量"])
                check.equal(data["IN_YARD_GTPKS"], expected_results[index]["剩余件数"])
                check.equal(data["IN_YARD_GTWG"], expected_results[index]["剩余重量"])


@allure.story('罗泾报表一期')
@allure.title('6.外贸出口船舶作业情况统计表')
@pytest.mark.parametrize("starttm,endtm", [('2023-04-01', '2023-04-17')])
def test_export_w(server_host, db_host, starttm, endtm):
    schema = read_json(os.path.join(os.getcwd(), r'schema\export_w.json'))
    with allure.step("接口请求"):
        r = InterfaceRes(server_host)
        res = r.test_export_w(schema, starttm, endtm)
    with allure.step("数据库请求"):
        d = DataRes(db_host)
        expected_results = d.export_w(starttm, endtm)
    with allure.step("数据比对"):
        expected_keys = [(data["船名"], data["航次"]) for data in expected_results]
        expected_indexs = {key: i for i, key in enumerate(expected_keys)}
        check.equal(len(expected_results)-1, len(res["data"]), "数据量不相等")
        for data in res["data"]:
            key = (data["vsl_cnname"], data["voy_voyage"])
            index = expected_indexs.get(key)
            check.is_not_none(index, "未匹配到数据: {}/{}".format(data["vsl_cnname"], data["voy_voyage"]))
            if index is not None:
                check.equal(data["bil_gtpks_total"], expected_results[index]["舱单件数"])
                check.equal(data["bil_gtwg_total"], expected_results[index]["舱单重量"])
                check.equal(data["tv_goa_gtpks"], expected_results[index]["车直装件数"])
                check.equal(data["tv_goa_gtwg"], expected_results[index]["车直装重量"])
                check.equal(data["bv_goa_gtpks"], expected_results[index]["驳直装件数"])
                check.equal(data["bv_goa_gtwg"], expected_results[index]["驳直装重量"])
                check.equal(data["yv_goa_gtpks"], expected_results[index]["库场装船件数"])
                check.equal(data["yv_goa_gtwg"], expected_results[index]["库场装船重量"])
                check.equal(data["ty_goa_gtpks"], expected_results[index]["库场进货件数"])
                check.equal(data["ty_goa_gtwg"], expected_results[index]["库场进货重量"])
                check.equal(data["e_in_yard_gtpks"], expected_results[index]["剩余件数"])
                check.equal(data["e_in_yard_gtwg"], expected_results[index]["剩余重量"])


@allure.story('罗泾报表一期')
@allure.title('7.分类定额效率统计表')
@pytest.mark.parametrize("start_date,end_date", [('2023-04-01', '2023-04-17')])
def test_quona_workpiece_ratio_count(server_host, db_host, start_date, end_date):
    schema = read_json(os.path.join(os.getcwd(), r'schema\quona_workpiece_ratio_count.json'))
    with allure.step("接口请求"):
        r = InterfaceRes(server_host)
        res = r.test_quona_workpiece_ratio_count(schema, start_date, end_date)
    with allure.step("数据库请求"):
        d = DataRes(db_host)
        expected_results = d.quona_workpiece_ratio_count(start_date, end_date)
    with allure.step("数据比对"):
        expected_keys = [(data["定额编号"]) for data in expected_results]
        expected_indexs = {key: i for i, key in enumerate(expected_keys)}
        check.equal(len(expected_results), len(res["data"]), "数据量不相等")
        for data in res["data"]:
            key = (data["rpt_wsw_quotano"])
            index = expected_indexs.get(key)
            check.is_not_none(index, "未匹配到数据: rpt_wsw_quotano = {}".format(data["rpt_wsw_quotano"]))
            if index is not None:
                check.equal(data["rpt_wsw_pws_no"], expected_results[index]["使用次数"])
                check.equal(data["rpt_pck_kind_name"], expected_results[index]["定额分类"])
                check.equal(data["rpt_opc_name"], expected_results[index]["操作过程"])
                check.equal(data["rpt_quo_time_quota"], expected_results[index]["工时定额"])
                check.equal(data["rpt_wsw_work_hours"], expected_results[index]["作业小时"])
                check.equal(data["rpt_wsw_gtwgs"], expected_results[index]["完成操作吨"])
                check.equal(data["rpt_quo_work_num"], expected_results[index]["定额装卸工人数"])
                check.equal(data["rpt_practical_work_num"], expected_results[index]["实际装卸工人数"])
                check.equal(data["rpt_quo_time_quotawork"], expected_results[index]["定额工时"])
                check.equal(data["rpt_wsw_real_hour"], expected_results[index]["实际工时"])
                check.equal(float(data["rpt_quo_hatch_hour"]), float(expected_results[index]["定额作业小时量"]))
                check.equal(data["rpt_wsw_gtwg_hour"], expected_results[index]["实际作业小时量"])
                check.equal(data["rpt_percentage_complete_quota"], expected_results[index]["定额完成率"])


@allure.story('罗泾报表一期')
@allure.title('8.保税仓库库场情况表')
def test_bondedcase_day(server_host, db_host):
    schema = read_json(os.path.join(os.getcwd(), r'schema\bondedcase_day.json'))
    with allure.step("接口请求"):
        r = InterfaceRes(server_host)
        res = r.test_bondedcase_day(schema)
    with allure.step("数据库请求"):
        d = DataRes(db_host)
        expected_results = d.bondedcase_day()
    with allure.step("数据比对"):
        expected_keys = [(data["船名"], data["航次"], data["提单号"]) for data in expected_results]
        expected_indexs = {key: i for i, key in enumerate(expected_keys)}
        check.equal(len(expected_results), len(res["data"]), "数据量不相等")
        for data in res["data"]:
            key = (data["vslname"], data["voyage"], data["billNbr"])
            index = expected_indexs.get(key)
            check.is_not_none(index, "未匹配到数据: vslname/voyage = {}/{},billNbr = {}"
                              .format(data["vslname"], data["voyage"], data["billNbr"]))
            if index is not None:
                check.equal(data["bod_no"], expected_results[index]["项号"])
                check.equal(data["goodsName"], expected_results[index]["货名"])
                check.equal(data["totalGoodsPieces"], expected_results[index]["总件数"])
                check.equal(data["totalGoodsWeight"], expected_results[index]["总重量"])
                check.equal(data["totalGoodsWeightNet"], expected_results[index]["总净重"])
                check.equal(data["inGoodsPieces"], expected_results[index]["进库件数"])
                check.equal(data["inGoodsWeight"], expected_results[index]["进库重量"])
                check.equal(data["outGoodsPieces"], expected_results[index]["出库件数"])
                check.equal(data["outGoodsWeight"], expected_results[index]["出库重量"])
                check.equal(data["storeGoodsPieces"], expected_results[index]["结存件数"])
                check.equal(data["storeGoodsWeight"], expected_results[index]["结存重量"])


@allure.story('罗泾报表一期')
@allure.title('9.保税仓库进出报表')
@pytest.mark.parametrize("start_date,end_date,bod_no,billNbr,vslname",
                         [('2023-04-01', '2023-04-17', '2', "CD20230410LJ004", "丽萨")])
def test_bondedio_day(server_host, db_host, start_date, end_date, bod_no, billNbr, vslname):
    schema = read_json(os.path.join(os.getcwd(), r'schema\bondedio_day.json'))
    with allure.step("接口请求"):
        r = InterfaceRes(server_host)
        res = r.test_bondedio_day(schema, start_date, end_date, bod_no, billNbr, vslname)
    with allure.step("数据库请求"):
        d = DataRes(db_host)
        expected_results = d.bondedio_day(start_date, end_date, bod_no, billNbr, vslname)
    with allure.step("数据比对"):
        expected_keys = [(data["船名"], data["航次"], data["提单号"]) for data in expected_results]
        expected_indexs = {key: i for i, key in enumerate(expected_keys)}
        check.equal(len(expected_results), len(res["data"]), "数据量不相等")
        for data in res["data"]:
            key = (data["vslname"], data["voyage"], data["billNbr"])
            index = expected_indexs.get(key)
            check.is_not_none(index, "未匹配到数据: vslname/voyage = {}/{},billNbr = {}"
                              .format(data["vslname"], data["voyage"], data["billNbr"]))
            if index is not None:
                check.equal(data["bod_no"], expected_results[index]["料号"])
                check.equal(data["bod_record_no"], expected_results[index]["序号"])
                check.equal(data["goodsName"], expected_results[index]["货名"])
                check.equal(data["totalGoodsPieces"], expected_results[index]["总件数"])
                check.equal(data["totalGoodsWeight"], expected_results[index]["总重量"])
                check.equal(data["totalGoodsWeightNet"], expected_results[index]["总净重"])
                check.equal(data["ygc_no"], expected_results[index]["货位"])
                check.equal(data["inGoodsPieces"], expected_results[index]["进库件数"])
                check.equal(data["inGoodsWeight"], expected_results[index]["进库重量"])
                check.equal(data["inGoodsWeightNet"], expected_results[index]["进库净重"])
                check.equal(data["bod_stock_date"], expected_results[index]["进库日期"])
                check.equal(data["outGoodsPieces"], expected_results[index]["出库件数"])
                check.equal(data["outGoodsWeight"], expected_results[index]["出库重量"])
                check.equal(data["outGoodsWeightNet"], expected_results[index]["出库净重"])
                check.equal(data["outdate"], expected_results[index]["出库日期"])
                check.equal(data["storeGoodsPieces"], expected_results[index]["结存件数"])
                check.equal(data["storeGoodsWeight"], expected_results[index]["结存重量"])
                check.equal(data["storeGoodsWeightNet"], expected_results[index]["结存净重"])


@allure.story('罗泾报表一期')
@allure.title('10.船舶工时表')
@pytest.mark.parametrize("start_date,end_date,pws_voy_id,route_sign",
                         [('2023-04-01', '2023-04-17', '6f3683616ec7f2a09087b634352a6538', '00018010')])
def test_shipworkhour(server_host, db_host, start_date, end_date, pws_voy_id, route_sign):
    schema = read_json(os.path.join(os.getcwd(), r'schema\shipworkhour.json'))
    with allure.step("接口请求"):
        r = InterfaceRes(server_host)
        res = r.test_shipworkhour(schema, start_date, end_date, pws_voy_id, route_sign)
    with allure.step("数据库请求"):
        d = DataRes(db_host)
        d.shipworkhour_wk(start_date, end_date, pws_voy_id, route_sign)
        expected_results = d.shipworkhour_machine(start_date, end_date, pws_voy_id, route_sign)
    with allure.step("数据比对"):
        expected_keys = [(data["航次"], data["作业路标识"], data["工号"]) for data in expected_results]
        expected_indexs = {key: i for i, key in enumerate(expected_keys)}
        check.equal(len(expected_results), len(res["data"]), "数据量不相等")
        for data in res["data"]:
            key = (data["pws_voy_id"], data["wsw_route_sign"], data["wsw_empno"])
            index = expected_indexs.get(key)
            check.is_not_none(index, "未匹配到数据: pws_voy_id = {}, wsw_route_sign = {},wsw_empno = {}"
                              .format(data["pws_voy_id"], data["wsw_route_sign"], data["wsw_empno"]))
            if index is not None:
                check.equal(data["wsm_gtpks"], expected_results[index]["件数"])
                check.equal(data["wsm_gtwg"], expected_results[index]["吨位"])
                check.equal(data["wsm_work_hour"], expected_results[index]["工作时间"])
                check.equal(data["wsm_truck_order"], expected_results[index]["车次"])
                check.equal(data["wsm_plus_minus_hour"], expected_results[index]["加减工时"])
                check.equal(data["wsm_adjust_factor"], expected_results[index]["调节系数"])
                check.equal(data["wsm_overtime_rate"], expected_results[index]["加班率"])
                check.equal(data["wsm_base_hour"], expected_results[index]["原始工时"])
                check.equal(data["wsm_real_hour"], expected_results[index]["折算工时"])



@allure.story('罗泾报表一期')
@allure.title('11.昼夜作业情况统计表')
@pytest.mark.parametrize("work_date", ['2023-04-17'])
def test_daynightworksta_day(server_host, db_host, work_date):
    schema = read_json(os.path.join(os.getcwd(), r'schema\daynightworksta_day.json'))
    with allure.step("接口请求"):
        r = InterfaceRes(server_host)
        res = r.test_daynightworksta_day(schema, work_date)
    with allure.step("数据库请求"):
        d = DataRes(db_host)
        expected_results1 = d.daynightworksta_day(work_date)
        expected_results2 = d.daynightworksta_zj(work_date)
        expected_results3 = d.daynightworksta_store(work_date)
        expected_results4 = d.daynightworksta_paper(work_date)
        expected_results5 = d.daynightworksta_nin(work_date)
    with allure.step("数据比对-桩脚"):
        expected_keys = [(data["场地区域"]) for data in expected_results2]
        expected_indexs = {key: i for i, key in enumerate(expected_keys)}
        for data in res["data"][1]:
            key = (data["ybkname"])
            index = expected_indexs.get(key)
            if index is not None:
                check.equal(data["ybkcount"], expected_results2[index]["桩脚"])
    with allure.step("数据比对-本日纸浆提货情况"):
        check.equal(res["data"][0][0]["wg"], expected_results4[0]["驳提纸浆重量"])
        check.equal(res["data"][0][0]["pks"], expected_results4[0]["驳提纸浆件数"])
        check.equal(res["data"][0][1]["wg"], expected_results4[0]["车提纸浆重量"])
        check.equal(res["data"][0][1]["pks"], expected_results4[0]["车提纸浆件数"])
    with allure.step("数据比对-本日内贸进场情况"):
        check.equal(res["data"][0][2]["wg"], expected_results5[0]["重量"])
        check.equal(res["data"][0][2]["pks"], expected_results5[0]["件数"])



@allure.story('罗泾报表一期')
@allure.title('12.船代外贸进出口')
@pytest.mark.parametrize("yyyy,mm", [('2023', '04')])
def test_vagt_wgood(server_host, db_host, yyyy, mm):
    schema = read_json(os.path.join(os.getcwd(), r'schema\vagt_wgood.json'))
    with allure.step("接口请求"):
        r = InterfaceRes(server_host)
        res = r.test_vagt_wgood(schema, yyyy, mm)
    with allure.step("数据库请求"):
        d = DataRes(db_host)
        expected_results = d.vagt_wgood(yyyy, mm)
    with allure.step("数据比对"):
        expected_keys = [(data["船代"]) for data in expected_results]
        expected_indexs = {key: i for i, key in enumerate(expected_keys)}
        check.equal(len(expected_results), len(res["data"]), "数据量不相等")
        for data in res["data"]:
            key = (data["cst_shrtnm"])
            index = expected_indexs.get(key)
            check.is_not_none(index, "未匹配到数据: cst_shrtnm = {}".format(data["cst_shrtnm"]))
            if index is not None:
                check.equal(data["wino"], expected_results[index]["外贸进口艘次"])
                check.almost_equal(data["wiwg"], expected_results[index]["外贸进口吨位"], 4)
                check.almost_equal(data["wibilwg"], expected_results[index]["外贸进口计费吨"], 4)
                check.equal(data["weno"], expected_results[index]["外贸出口艘次"])
                check.almost_equal(data["wewg"], expected_results[index]["外贸出口吨位"], 4)
                check.almost_equal(data["webilwg"], expected_results[index]["外贸出口计费吨"], 4)
                check.equal(data["totalno"], expected_results[index]["合计艘次"])
                check.almost_equal(data["totalwg"], expected_results[index]["合计吨位"], 4)
                check.almost_equal(data["totalbilwg"], expected_results[index]["合计计费吨"], 4)
                check.equal(data["yearno"], expected_results[index]["年度合计艘次"])
                check.almost_equal(data["yearwg"], expected_results[index]["年度合计吨位"], 4)
                check.almost_equal(data["yearbilwg"], expected_results[index]["年度合计计费吨"], 4)



@allure.story('罗泾报表一期')
@allure.title('13.航线统计表')
@pytest.mark.parametrize("yyyy", ['2023'])
def test_voyage_count(server_host, db_host, yyyy):
    schema = read_json(os.path.join(os.getcwd(), r'schema\voyage_count.json'))
    with allure.step("接口请求"):
        r = InterfaceRes(server_host)
        r.test_voyage_count(schema, yyyy)
    with allure.step("数据库请求"):
        d = DataRes(db_host)
        d.voyage_count(yyyy)


@allure.story('罗泾报表一期')
@allure.title('14.船公司外贸进出口')
@pytest.mark.parametrize("work_date", ['2023-04-17'])
def test_boatcompany_day(server_host, db_host, work_date):
    schema = read_json(os.path.join(os.getcwd(), r'schema\boatcompany_day.json'))
    with allure.step("接口请求"):
        r = InterfaceRes(server_host)
        res = r.test_boatcompany_day(schema, work_date)
    with allure.step("数据库请求"):
        d = DataRes(db_host)
        expected_results = d.boatcompany_day(work_date)
    with allure.step("数据比对"):
        expected_keys = [(data["船公司"]) for data in expected_results]
        expected_indexs = {key: i for i, key in enumerate(expected_keys)}
        for data in res["data"]:
            key = (data["bmname"])
            index = expected_indexs.get(key)
            if index is not None:
                check.equal(data["icoun"], expected_results[index]["进口艘次"])
                check.equal(data["ecoun"], expected_results[index]["出口艘次"])
                check.equal(data["totcoun"], expected_results[index]["合计艘次"])
                check.equal(data["YEARtotcoun"], expected_results[index]["年度合计艘次"])
                check.almost_equal(data["weironwg"], expected_results[index]["外出钢材"], 4)
                check.almost_equal(data["weequipwg"], expected_results[index]["外出设备"], 4)
                check.almost_equal(data["wedwg"], expected_results[index]["外出吨袋货"], 4)
                check.almost_equal(data["weothwg"], expected_results[index]["外出其他"], 4)
                check.almost_equal(data["wipapwg"], expected_results[index]["外进纸浆"], 4)
                check.almost_equal(data["wiironwg"], expected_results[index]["外进钢材"], 4)
                check.almost_equal(data["wiequipwg"], expected_results[index]["外进设备"], 4)
                check.almost_equal(data["wiwoodwg"], expected_results[index]["外进原木"], 4)
                check.almost_equal(data["wiothwg"], expected_results[index]["外进其他"], 4)
                check.almost_equal(data["YEARwwg"], expected_results[index]["年度合计吨位"], 4)



@allure.story('罗泾报表一期')
@allure.title('15.主要货种完成量')
@pytest.mark.parametrize("yyyy", ['2023'])
def test_maingoods_dclddtl(server_host, db_host, yyyy):
    schema = read_json(os.path.join(os.getcwd(), r'schema\maingoods_dclddtl.json'))
    with allure.step("接口请求"):
        r = InterfaceRes(server_host)
        r.test_maingoods_dclddtl(schema, yyyy)
    with allure.step("数据库请求"):
        d = DataRes(db_host)
        d.maingoods_dclddtl(yyyy)
