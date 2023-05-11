# -*- coding:utf-8 -*-
# Developer         : baishijun
# Development Time  : 2023/5/9 9:44
# Document Name     : deliver_w.PY
# Development Tool  : PyCharm

import json
import random
from pytest_check import check
from BTOSLJ.Controls.BTOS_requests import RequestMain
from BTOSLJ.Controls.BTOS_db import GetPg
from BTOSLJ.Controls.BTOS_data import BtosTempData, BtosCustomData
import os


class DeliverW(RequestMain):

    def __init__(self, host, header):
        super().__init__(host, header)
        self.env = BtosTempData(os.path.join(os.path.dirname(__file__) + r"\Excel\test_env_e_w.yaml"))
        self.cus = BtosCustomData()
        self.db = GetPg("10.166.0.137")

    def set_values(self):
        self.env.term_cd = 'L'  # 作业区
        gtypecd, pktype = self.cus.get_pktype
        self.env.gtypecd = gtypecd  # 货类代码
        self.env.gname = \
            self.db.select_from_table("select pck_kind_name "
                                      "from pub_cargo_kind "
                                      "where pck_kind_code='{gtypecd}'"
                                      .format(gtypecd=self.env.gtypecd)).loc[0, 'pck_kind_name']  # 货名
        self.env.pktype = pktype  # 包装代码
        self.env.pkname = \
            self.db.select_from_table("select pkg_cnname "
                                      "from pub_package "
                                      "where pkg_code='{pktype}' "
                                      .format(pktype=self.env.pktype)).loc[0, 'pkg_cnname']  # 包装名称
        self.env.voyage = self.cus.get_Evoyage  # 航次
        self.env.trade_type = 'W'  # 贸易类型
        self.env.gtwg = self.cus.get_gtwg  # 重量
        self.env.gtpks = self.cus.get_gtpks  # 件数
        self.env.gtvol = self.cus.get_gtvol  # 体积
        self.env.iefg = 'E'  # 进出口
        self.env.shift = '1'  # 工班代码
        self.env.opproc_de_w = '002'  # 车=>场
        self.env.opproc_de_b = 'B002'  # 驳=>场
        self.env.opproc_ld = '016'  # 场=>船
        ygc_list = self.db.select_from_table("select ygc_no "
                                             "from pub_yard_goods_location "
                                             "where tenant_id = 'SIPGLJ'")
        self.env.ygc_no = ygc_list.loc[random.randint(0, len(ygc_list) - 1), 'ygc_no']  # 货位名称
        self.env.ygc_id = \
            self.db.select_from_table("select ygc_id "
                                      "from pub_yard_goods_location "
                                      "where ygc_no='{ygc_no}' "
                                      .format(ygc_no=self.env.ygc_no)).loc[0, 'ygc_id']  # 货位id
        self.env.optype_de = 'DE'  # 进货作业方式代码
        self.env.optype_ld = 'LD'  # 装船作业方式代码
        apply_unit_list = \
            self.db.select_from_table("select cst_id ,cst_cstmnm "
                                      "from pub_customers cst "
                                      "join pub_customers_role ctr on cst.cst_id = ctr.ctr_cst_id "
                                      "and cst.tenant_id = ctr.tenant_id "
                                      "where ctr.ctr_cst_type = 'AGT' and cst.tenant_id = 'SIPGLJ'")
        r1 = random.randint(0, len(apply_unit_list) - 1)
        self.env.agent_id = apply_unit_list.loc[r1, 'cst_id']  # 货代id
        self.env.agent_name = apply_unit_list.loc[r1, 'cst_cstmnm']  # 货代名称
        owner_list = \
            self.db.select_from_table("select cst_id ,cst_cstmnm "
                                      "from pub_customers cst "
                                      "join pub_customers_role ctr on cst.cst_id = ctr.ctr_cst_id "
                                      "and cst.tenant_id = ctr.tenant_id "
                                      "where ctr.ctr_cst_type = 'AGT' and cst.tenant_id = 'SIPGLJ'")
        r5 = random.randint(0, len(owner_list) - 1)
        self.env.owner_id = owner_list.loc[r5, 'cst_id']  # 货主id
        self.env.owner_name = owner_list.loc[r5, 'cst_cstmnm']  # 货主名称
        vagent_list = \
            self.db.select_from_table("select cst_id ,cst_cstmnm, cst_cstmcd "
                                      "from pub_customers cst "
                                      "join pub_customers_role ctr on cst.cst_id = ctr.ctr_cst_id "
                                      "and cst.tenant_id = ctr.tenant_id "
                                      "where ctr.ctr_cst_type = 'VAGT' and cst.tenant_id = 'SIPGLJ'")
        r2 = random.randint(0, len(vagent_list) - 1)
        self.env.vagent_id = vagent_list.loc[r2, 'cst_id']  # 船代id
        self.env.vagent_name = vagent_list.loc[r2, 'cst_cstmnm']  # 船代名称
        self.env.vagent_code = vagent_list.loc[r2, 'cst_cstmcd']  # 船代代码
        service_line_list = self.db.select_from_table("select sln_code "
                                                      "from pub_service_lines "
                                                      "where tenant_id = 'SIPGLJ'")
        self.env.service_line = service_line_list.loc[random.randint(0, len(service_line_list) - 1), 'sln_code']  # 航线代码
        bth_list = self.db.select_from_table("select bth_bthno ,bth_startpst "
                                             "from bps_berthes "
                                             "where tenant_id = 'SIPGLJ'")
        r3 = random.randint(0, len(bth_list) - 1)
        self.env.bth_no = bth_list.loc[r3, 'bth_bthno']  # 泊位代码
        self.env.bth_startpst = float(bth_list.loc[r3, 'bth_startpst'])  # 泊位起始尺码
        flow_list = self.db.select_from_table("select reg_code "
                                              "from pub_region "
                                              "where reg_cty_id<>'CN' and tenant_id='SIPGLJ'")
        self.env.flow_direct = flow_list.loc[random.randint(0, len(flow_list) - 1), "reg_code"]  # 流向
        self.env.craft_de = 'JINHUO'
        self.env.craft_ld = ''

    def get_user(self):
        self.env.user_cnname = "罗泾管理员"
        payload = {
            "orderItems": "createTime DESC",
            "name": self.env.user_cnname,
            "phone": "",
            "total": 1,
            "size": 20,
            "current": 1
        }
        res = self.request_main("GET", "/auth/saas/tenant/user/page", params=payload)
        data = res.json()
        if check.equal(int(data["status"]), 200):
            self.env.user_id = data["data"]["records"][0]["id"]
            self.env.user_enname = data["data"]["records"][0]["account"]
            self.env.emp_no = data["data"]["records"][0]["empNumber"]
            self.env.user_dept_id = data["data"]["records"][0]["depts"][0]["deptId"]
            self.env.user_dept_name = data["data"]["records"][0]["depts"][0]["deptName"]
        else:
            self.logger.error("获取用户信息失败")

    def add_vessel(self):
        self.env.vsl_cd = "REQUEST TEST E"
        self.env.vsl_cnname = "接口测试船E"
        self.env.vsl_enname = "REQUEST TEST E"
        self.env.vsl_loa = 150
        payload = {
            "vslCd": self.env.vsl_cd,
            "vslVtpcode": "CAS",
            "vslCnname": self.env.vsl_cnname,
            "vslEnname": self.env.vsl_enname,
            "vslCallsign": "",
            "vslCtyCountrycd": "CN",
            "vslCstShippingline": "CHPO",
            "vslCstAgency": "BWHY",
            "vslLoa": self.env.vsl_loa,
            "vslBreadth": "",
            "vslGton": "1000",
            "vslNetton": "800",
            "vslTotallocation": "",
            "vslSummaryloading": "",
            "vslBaynum": 0,
            "vslDraftunload": "",
            "vslDraftload": "",
            "vslDeckmaxtiers": 0,
            "vslDeckmaxrows": 0,
            "vslHatchamount": "5",
            "vslHatchcoveramount": "",
            "vslHatchmaxtiers": 0,
            "vslHatchmaxrows": 0,
            "vslDerrickamount": "",
            "vslBkbaynum": 0,
            "vslRfsocket": "",
            "vslMadedt": self.cus.get_datetime_now,
            "vslDepth": "",
            "vslSailspeed": "",
            "vslStowagereq": "",
            "vslLoaddisargereq": "",
            "vslCallid": "",
            "vslBkstartbay": "",
            "vslBkendbay": "",
            "vslOrigin": "",
            "vslEndlength": "",
            "vslVcg": "",
            "vslLcg": "",
            "vslTcg": "",
            "vslSpoptp": "",
            "vslAudio": "",
            "vslPilotage": "",
            "vslUncode": "",
            "vslStopsign": "Y",
            "vslStdId": "",
            "vslBksternnum": "",
            "vslImono": "123456",
            "form": "vslImono"
        }
        res = self.request_main('POST', '/tos/bps/vessels', json=payload)
        data = res.json()
        if check.equal(int(data["status"]), 200):
            self.env.vsl_id = data["data"]["vslId"]
        else:
            self.logger.error("新增船舶失败")

    def delete_vessel(self):
        res = self.request_main('DELETE', '/tos/bps/vessels/{vsl_id}'.format(vsl_id=self.env.vsl_id))
        data = res.json()
        check.equal(int(data["status"]), 200)

    def add_schedule(self):
        self.env.scd_eta = self.cus.get_datetime_now
        self.env.scd_etd = self.cus.get_datetime_add(self.env.scd_eta, day=2)
        payload = {
            "scdVslId": self.env.vsl_id,
            "scdVslCd": self.env.vsl_cd,
            "vslCnname": self.env.vsl_cnname,
            "vslLoa": self.env.vsl_loa,
            "vslBreadth": 0,
            "vslGton": 1000,
            "vslNetton": 800,
            "scdEta": self.env.scd_eta,
            "scdEtd": self.env.scd_etd,
            "scdPriorport": "",
            "scdNextport": "",
            "scdAta": "",
            "scdFixscdshpfg": "N",
            "scdTermcd": "",
            "bpsIvoyageQuery": {
                "scdIvoyageId": "",
                "scdIvoyageSn": "",
                "scdIvoyage": "",
                "scdGoodsIlists": [],
                "scdIton": "",
                "scdIowner": "",
                "scdIvagt": "",
                "scdIagtContact": "",
                "scdIvoyTrade": ""
            },
            "bpsEvoyageQuery": {
                "scdEvoyageId": "",
                "scdEvoyageSn": self.env.service_line,
                "scdEvoyage": self.env.voyage,
                "scdGoodsElists": [self.env.gtypecd],
                "scdEton": self.env.gtwg,
                "scdEowner": "",
                "scdEvagt": self.env.vagent_code,
                "scdEagtContact": "bsj",
                "scdEvoyTrade": self.env.trade_type
            },
            "bpsShipScheduleEditingVOList": [],
            "scdStatus": 1,
            "scdTerStatus": 0,
            "scdIagtContact": "",
            "scdEagtContact": "bsj",
            "scdIton": None,
            "scdEton": self.env.gtwg
        }
        res = self.request_main('POST', '/tos/bps/schedule', json=payload)
        data = res.json()
        if check.equal(int(data["status"]), 200):
            self.env.scd_id = data["data"]["scdId"]
            self.env.voy_id = \
                self.db.select_from_table("select voy_id from bps_voyage "
                                          "where voy_scd_id='{scd_id}' and voy_voyage='{voyage}' "
                                          .format(scd_id=self.env.scd_id, voyage=self.env.voyage)).loc[0, 'voy_id']
        else:
            self.logger.error("新增船期失败")

    def delete_schedule(self):
        res = self.request_main('DELETE', '/tos/bps/schedule/{scd_id}'.format(scd_id=self.env.scd_id))
        data = res.json()
        check.equal(int(data["status"]), 200)

    def confirm_report(self):
        payload = {
            "scdId": [self.env.scd_id],
            "scdTermcd": "",
            "scdStatus": 1,
            "scdTerStatus": ""
        }
        res = self.request_main('POST', '/tos/bps/schedule/updateScdStatus', json=payload)
        data = res.json()
        check.equal(int(data["status"]), 200)

    def confirm_report_cancel(self):
        payload = {
            "scdId": [self.env.scd_id],
            "scdTermcd": "",
            "scdStatus": 2,
            "scdTerStatus": ""
        }
        res = self.request_main('POST', '/tos/bps/schedule/updateScdStatus', json=payload)
        data = res.json()
        check.equal(int(data["status"]), 200)

    def subarea(self):
        payload = {
            "scdId": [self.env.scd_id],
            "scdTermcd": self.env.term_cd,
            "scdStatus": 2,
            "scdTerStatus": "1"
        }
        res = self.request_main('POST', '/tos/bps/schedule/updateScdStatus', json=payload)
        data = res.json()
        check.equal(int(data["status"]), 200)

    def subarea_cancel(self):
        payload = {
            "scdId": [self.env.scd_id],
            "scdTermcd": "",
            "scdStatus": 2,
            "scdTerStatus": "0"
        }
        res = self.request_main('POST', '/tos/bps/schedule/updateScdStatus', json=payload)
        data = res.json()
        check.equal(int(data["status"]), 200)

    def add_berth_plan(self):
        self.env.vbt_pbthdt = self.cus.get_datetime_now
        self.env.vbt_pdptdt = self.cus.get_datetime_add(self.env.vbt_pbthdt, day=1)
        payload = {
            "vbtScdId": self.env.scd_id,
            "vbtId": "",
            "vbtTermcd": self.env.term_cd,
            "vbtPstpst": self.env.bth_startpst,
            "vbtPedpst": self.env.bth_startpst + self.env.vsl_loa,
            "vbtPbthdirect": "L",
            "vbtBthPbthno": "{},{}".format(self.env.bth_no, self.env.bth_no),
            "vbtEndBthPbthno": self.env.bth_no,
            "vbtPbthdt": self.env.vbt_pbthdt,
            "vbtPdptdt": self.env.vbt_pdptdt,
            "vbtPbthdraft": "20",
            "vbtPdptdraft": "10",
            "bowPiles": [],
            "sternPiles": [],
            "vbbIdPlan": []
        }
        res = self.request_main('PUT', '/tos/bps/terminalMonitoring/updateBertdrawing', json=payload)
        data = res.json()
        check.equal(int(data["status"]), 200)

    # 新增进货受理,车进
    def add_accept_w(self):
        self.env.dwp_type = 'W'
        self.env.pln_opsttm = self.cus.get_datetime_add(self.cus.to_date(self.cus.get_datetime_now), hour=18)
        self.env.pln_opedtm = self.cus.get_datetime_add(self.env.pln_opsttm, day=1)
        self.env.bill_no = self.cus.get_bill
        self.env.mark_no = self.cus.get_mark
        self.env.ht_no = self.cus.get_ht
        payload = {
            "plnTransmode": self.env.optype_de,
            "pasPlanAppendix": [],
            "plnVoyId": self.env.voy_id,
            "inStack": "false",
            "plnOpsttm": self.env.pln_opsttm,
            "plnOpedtm": self.env.pln_opedtm,
            "plnStatus": "P",
            "operationProcess": [self.env.opproc_de_w],
            "pasPlansExtendEntity": {
                "ppeAuthCode": "",
                "ppePrintState": "N"
            },
            "plnTel": self.cus.get_phone,
            "plnRemark": "外贸进货受理-备注",
            "plnThrType": "1",  # 受理单位，0货主，1货代
            "plnConsignee": "bsj",  # 联系人
            "plnApplyUnit": self.env.agent_id,
            "plnDirect": self.env.flow_direct,
            "plnTruckNum": "1",  # 车数
            "plnGtpks": self.env.gtpks,
            "plnGtwg": self.env.gtwg,
            "plnIefg": self.env.iefg,
            "plnTrade": self.env.trade_type,
            "plnTermcd": self.env.term_cd,
            "plnOverSize": "N",
            "plnPreDelivery": "N",
            "pasPlanGoodsEntities": [
                {
                    "plgBillno": self.env.bill_no,
                    "plgMarkerno": self.env.mark_no,
                    "plgContractNo": self.env.ht_no,
                    "plgGtypecd": self.env.gtypecd,
                    "plgGname": self.env.gname,
                    "plgOwnerId": self.env.owner_id,
                    "plgOpPlaces": [
                        "0"
                    ],
                    "plgPGtpks": self.env.gtpks,
                    "plgPGtwg": self.env.gtwg,
                    "plgPktype": self.env.pktype,
                    "plgPGtvol": self.env.gtvol,
                    "plgRemark": "货物备注",
                    "plgShipper": "",
                    "id": "",
                    "_XID": "row_551",
                    "plgVoyId": self.env.voy_id,
                    "plgAgentId": self.env.agent_id
                }
            ],
            "pasBargeBerthList": []
        }
        res = self.request_main('POST', '/tos/pas/plans', json=payload)
        data = res.json()
        if check.equal(int(data["status"]), 200):
            self.env.pln_id = data["data"]["plnId"]
            self.env.pln_no = data["data"]["plnPlanno"]
        else:
            self.logger.error("新增进货受理失败")

    def delete_accept(self):
        res = self.request_main('DELETE', '/tos/pas/plans/{pln_id}'.format(pln_id=self.env.pln_id))
        data = res.json()
        check.equal(int(data["status"]), 200)

    def add_warehouse_plan(self):
        self.env.dwp_opsttm = self.cus.get_datetime_add(self.cus.to_date(self.cus.get_datetime_now), day=-1)
        self.env.dwp_opedtm = self.cus.get_datetime_add(self.env.dwp_opsttm, day=2, hour=18)
        payload = {
            "dwpPlnId": self.env.pln_id,
            "dwpPlanno": self.env.pln_no,
            "dwpOpsttm": self.env.dwp_opsttm,
            "dwpOpedtm": self.env.dwp_opedtm,
            "dwpOwnerId": None,
            "dwpAgentId": self.env.agent_id,
            "dwpTermcd": self.env.term_cd,
            "dwpRemark": "外贸进货受理-备注",
            "dtsWarehouseRouteEntityList": [
                {
                    "dwrShiftNo": "1",
                    "pscOrder": 0,
                    "shiftName": "夜班",
                    "dwrRouteNum": "1",
                    "dwrOpton": self.env.gtwg,
                    "dwrKeyRpute": "N",
                    "dwrThroughput": "N",
                    "dwrType": "",
                    "dwrZxFlag": "N",
                    "dwrOpproc": self.env.opproc_de_w,
                    "dwrCraft": self.env.craft_de,
                    "dwrTermcd": "",
                    "jxts": "",
                    "zycl": "",
                    "dtsRouteWkgroupEntityList": [
                        {
                            "drwDeptId": "b20000daceb342798d22d4499077647d",
                            "drwWorkerNum": "3"
                        }
                    ]
                },
                {
                    "dwrShiftNo": "2",
                    "pscOrder": 1,
                    "shiftName": "日班",
                    "dwrRouteNum": "0",
                    "dwrOpton": "",
                    "dwrKeyRpute": "N",
                    "dwrThroughput": "N",
                    "dwrType": "",
                    "dwrZxFlag": "N",
                    "dwrOpproc": "",
                    "dwrCraft": "",
                    "dwrTermcd": "",
                    "jxts": "",
                    "zycl": "",
                    "dtsRouteWkgroupEntityList": []
                }
            ],
            "plnOpproc": self.env.opproc_de_w,
            "plnTransmode": self.env.optype_de,
            "dwrIds": []
        }
        res = self.request_main('POST', '/tos/dts/warehousePlan', json=payload)
        data = res.json()
        if check.equal(int(data["status"]), 200):
            self.env.dwp_id = data["data"]["dwpId"]
            self.env.dwr_id = data["data"]["dtsWarehouseRouteEntityList"][0]["dwrId"]
        else:
            self.logger.error("新增车驳作业计划失败")

    def delete_warehouse_plan(self):
        res = self.request_main('DELETE', '/tos/dts/warehousePlan/{dwp_id}'.format(dwp_id=self.env.dwp_id))
        data = res.json()
        check.equal(int(data["status"]), 200)

    def add_shift_task_de(self):
        self.env.dst_opdate = self.cus.to_date(self.cus.get_datetime_now)
        payload = {
            "dtsShiftTaskEntities": [
                {
                    "dstRouteId": self.env.dwr_id,
                    "dstTaskType": self.env.dwp_type,
                    "dstOpdate": self.env.dst_opdate,
                    "dstShiftCode": self.env.shift,
                    "dstOpproc": self.env.opproc_de_w,
                    "dstBerthno": "{},{}".format(self.env.bth_no, self.env.bth_no),
                    "dstCraft": self.env.craft_de,
                    "dstOptype": self.env.optype_de,
                    "dstPWgt": self.env.gtwg,
                    "dstAWgt": 0,
                    "dstHatchNo": "",
                    "dstHatchList": [],
                    "dstCargo": self.env.gtypecd,
                    "dstPktype": self.env.pktype,
                    "dstPmGroup": "",
                    "dstYardNote": "",
                    "dstSecurityNote": "",
                    "dstRemark": "外贸进货受理-备注|",
                    "dtoUserIdList": [],
                    "dstStopFlag": "N",
                    "dstKeyTask": "N",
                    "dstSheetStatus": "0",
                    "dstRouteStatus": "N",
                    "dstTermcd": self.env.term_cd,
                    "dstVoyId": "",
                    "dstPlnId": "",
                    "dstOutVoy": "",
                    "dstOutHatch": "",
                    "shiftTaskMactypeEntities": [],
                    "stmIds": [],
                    "shiftTaskWkgroupEntities": [
                        {
                            "stwWorkerNum": 3,
                            "stwGroup": "",
                            "stwPosType": "LJZD",
                            "stwPricingMode": "1",
                            "stwDeptId": "b20000daceb342798d22d4499077647d",
                            "stwPTons": "0"
                        }
                    ],
                    "stwIds": []
                }
            ],
            "dstIds": []
        }

        res = self.request_main('POST', '/tos/dts/shiftTask/stored', json=payload)
        data = res.json()
        if check.equal(int(data["status"]), 200):
            self.env.dst_id_de = data["data"][0]["dstId"]
            self.env.stw_id_de = data["data"][0]["shiftTaskWkgroupEntities"][0]["stwId"]
        else:
            self.logger.error("新增进货任务失败")

    def delete_shift_task(self, task_type):
        dst_id = self.env.dst_id_de if task_type == 'de' else self.env.dst_id_ld
        res = self.request_main('DELETE', '/tos/dts/shiftTask/{dst_id}'.format(dst_id=dst_id))
        data = res.json()
        check.equal(int(data["status"]), 200)

    def tally_attend(self):
        payload = {
            "dtsAttdWorkerEntities": [
                {
                    "dawEmpNo": self.env.emp_no,
                    "dawUserName": self.env.user_cnname,
                    "dawUserId": self.env.user_id,
                    "dawDeptName": self.env.user_dept_name,
                    "dawDeptId": self.env.user_dept_id,
                    "dawDate": self.env.dst_opdate,
                    "dawShift": self.env.shift,
                    "tagName": None,
                    "_XID": "row_2695"
                }
            ],
            "dawIds": [
                ""
            ]
        }
        res = self.request_main("POST", "/tos/dts/attdWorker/stored", json=payload)
        data = res.json()
        check.equal(int(data["status"]), 200)

    def tally_attend_cancel(self):
        # 理货员出勤id
        self.env.daw_id = \
            self.db.select_from_table("select daw_id "
                                      "from dts_attd_worker "
                                      "where daw_date = '{date}' and daw_shift = '{shift}' and daw_user_id = '{id}'"
                                      .format(date=self.env.dst_opdate, shift=self.env.shift, id=self.env.user_id)).loc[
                0, 'daw_id']
        payload = {
            "dtsAttdWorkerEntities": [],
            "dawIds": [self.env.daw_id]
        }
        res = self.request_main("POST", "/tos/dts/attdWorker/stored", json=payload)
        data = res.json()
        check.equal(int(data["status"]), 200)

    def tally_arrange(self, task_type):
        dst_id = self.env.dst_id_de if task_type == 'de' else self.env.dst_id_ld
        payload = {
            "dtsShiftTaskTallyEntityList": [
                {
                    "sttDstId": dst_id,
                    "sttUserId": self.env.user_id,
                    "sttUserNm": self.env.user_cnname,
                    "sttNunber": self.env.emp_no,
                    "sttGroup": None,
                    "sttRemark": "",
                    "createUser": None,
                    "createTime": None,
                    "updateUser": None,
                    "updateTime": None,
                    "_XID": "row_2754"
                }
            ]
        }
        res = self.request_main("POST", "/tos/dts/shiftTaskTally", json=payload)
        data = res.json()
        if check.equal(int(data["status"]), 200):
            if task_type == 'de':
                self.env.stt_id_de = data["data"]["dtsShiftTaskTallyEntityList"][0]["sttId"]
            else:
                self.env.stt_id_ld = data["data"]["dtsShiftTaskTallyEntityList"][0]["sttId"]
        else:
            self.logger.error("理货员安排失败")

    def tally_arrange_remove(self, task_type):
        stt_id = self.env.stt_id_de if task_type == 'de' else self.env.stt_id_ld
        payload = {
            "sttIds": [stt_id]
        }
        res = self.request_main("DELETE", "/tos/dts/shiftTaskTally/removeDtsAttworks", json=payload)
        data = res.json()
        check.equal(int(data["status"]), 200)

    def workgroup_arrange(self, task_type):
        stw_id = None
        dst_id = None
        config = None
        if task_type == 'ld':
            stw_id = self.env.stw_id_ld
            dst_id = self.env.dst_id_ld
            config = self.env.instructor_config
        elif task_type == 'de':
            self.env.tally_config = \
                self.db.select_from_table("select stc_id "
                                          "from dts_shift_task_config "
                                          "where stc_dts_id='{dst_id}' and stc_type='1'"
                                          .format(dst_id=self.env.dst_id_de)).loc[0, 'stc_id']
            stw_id = self.env.stw_id_de
            dst_id = self.env.dst_id_de
            config = self.env.tally_config
        payload = {
            "dtsShiftTaskWkgroupList": [
                {
                    "version": 1,
                    "createTime": self.cus.get_datetime_now,
                    "createUser": self.env.user_cnname,
                    "updateUser": None,
                    "updateTime": None,
                    "tenantId": "SIPGLJ",
                    "stwId": stw_id,
                    "stwDstId": dst_id,
                    "stwWorkerNum": 3,
                    "stwPlanWorkerNum": None,
                    "stwGroup": "LJAHD6-601",
                    "stwGroupNm": "601",
                    "stwPosType": "LJZD",
                    "stwPosTypeNm": "罗泾终点",
                    "stwPricingMode": "1",
                    "stwPricingModeNm": "计件",
                    "stwDeptId": "b20000daceb342798d22d4499077647d",
                    "stwDeptNm": "601",
                    "stwDeptCode": None,
                    "stwPTons": 0,
                    "stcId": None,
                    "dwkId": None,
                    "dtsShiftTaskWkgroupList": None,
                    "dtsShiftTaskConfigMacusrEntity": {
                        "tcmStcId": config
                    },
                    "stwIds": None,
                    "stwRGtwg": 0,
                    "stwRGtpks": 0,
                    "_XID": "row_1441"
                }
            ]
        }
        res = self.request_main("PUT", "/tos/dts/shiftTaskConfigMacusr/updateShiftWkgroup", json=payload)
        data = res.json()
        check.equal(int(data["status"]), 200)

    def workgroup_arrange_delete(self, task_type):
        stw_id = None
        config = None
        if task_type == 'ld':
            stw_id = self.env.stw_id_ld
            config = self.env.instructor_config
        elif task_type == 'de':
            stw_id = self.env.stw_id_de
            config = self.env.tally_config
        payload = {
            "stdId": [],
            "stwIds": [stw_id],
            "tcmStcIds": [config]
        }
        res = self.request_main("DELETE", "/tos/dts/shiftTaskConfigMacusr/deleteConfigMacusr", json=payload)
        data = res.json()
        check.equal(int(data["status"]), 200)

    def add_stack_prerecording(self):
        self.env.truck_no = self.cus.get_license_plate
        self.env.plg_id = self.db.select_from_table("select plg_id "
                                                    "from pas_plan_goods "
                                                    "where plg_pln_id = '{pln_id}'"
                                                    .format(pln_id=self.env.pln_id)).loc[0, "plg_id"]
        payload = {
            "sprTruckno": self.env.truck_no,
            "sprPlanno": self.env.pln_no,
            "gtsStackPrerecordingDtlEntityList": [
                {
                    "prefixTruck": self.env.truck_no[0],
                    "sprTruckno": self.env.truck_no,
                    "wverVehicleNo": self.env.truck_no[1:],
                    "sprPlanno": self.env.pln_no,
                    "sprDriver": "",
                    "sprPhone": "",
                    "sprPlnId": "",
                    "opprocCode": "",
                    "spdBillno": self.env.bill_no,
                    "spdMarkerno": self.env.mark_no,
                    "spdPieceNo": "",
                    "spdGname": self.env.gname,
                    "spdPktype": self.env.pktype,
                    "spdGtpks": self.env.gtpks,
                    "spdGtwg": self.env.gtwg,
                    "spdGtvol": self.env.gtvol,
                    "spdGlength": 0,
                    "spdGwidth": 0,
                    "spdGheight": 0,
                    "spdContractNo": self.env.ht_no,
                    "spdGtypecd": self.env.gtypecd,
                    "spdPlgId": self.env.plg_id
                }
            ]
        }
        res = self.request_main("POST", "/tos/gts/stackPrerecording", json=payload)
        data = res.json()
        if check.equal(int(data["status"]), 200):
            self.env.spr_id = data["data"]["gtsStackPrerecordingDtlEntityList"][0]["spdSprId"]
        else:
            self.logger.error("新增进栈预录失败")

    def delete_stack_prerecording(self):
        res = self.request_main("DELETE", "/tos/gts/stackPrerecording/{spr_id}".format(spr_id=self.env.spr_id))
        data = res.json()
        check.equal(int(data["status"]), 200)

    def in_door_check(self):
        payload = {
            "truckno": self.env.truck_no,
            "planno": self.env.pln_no
        }
        res = self.request_main("POST", "/tos/gts/stackPrerecordingDtl/planno/list", json=payload)
        data = res.json()
        check.equal(int(data["status"]), 200)

    def in_door_pass(self):
        payload = {
            "planno": [
                {
                    "planno": self.env.pln_no,
                    "remark": ""
                }
            ],
            "gatno": "1",
            "trkno": self.env.truck_no
        }
        res = self.request_main("POST", "/tos/gts/outtruckRecord/inpass", json=payload)
        data = res.json()
        if check.equal(int(data["status"]), 200):
            self.env.otr_id = \
                self.db.select_from_table("select otr_id "
                                          "from gts_outtruck_record "
                                          "where otr_truckno ='{truck_no}'"
                                          .format(truck_no=self.env.truck_no)).loc[0, 'otr_id']
        else:
            self.logger.error("进门道口放行失败")

    def out_door_pass(self):
        payload = {
            "otrId": self.env.otr_id,
            "outGatno": "4"
        }
        res = self.request_main("POST", "/tos/gts/outtruckRecord/outpass", json=payload)
        data = res.json()
        check.equal(int(data["status"]), 200)

    def tally_report_de(self, dwp_type):
        opproc_de = self.env.opproc_de_w if dwp_type == 'W' else self.env.opproc_de_b
        self.env.barcode_de = \
            self.db.select_from_table("select plg_bar_code "
                                      "from pas_plan_goods "
                                      "where plg_id = '{plg_id}' "
                                      .format(plg_id=self.env.plg_id)).loc[0, 'plg_bar_code']
        payload = {
            "barCode": self.env.barcode_de,
            "planNo": self.env.pln_no,
            "billNo": self.env.bill_no,
            "length": "0",
            "width": "0",
            "height": "0",
            "empId": self.env.user_id,
            "markNo": self.env.mark_no,
            "gateId": self.env.otr_id,
            "truckNo": self.env.truck_no,
            "flatCarNo": "",
            "cargoKind": self.env.gtypecd,
            "contractNo": self.env.ht_no,
            "pieceNo": "",
            "pieceCode": "",
            "damage": "0",
            "cntrNo": "",
            "wbFlag": "N",
            "specs": "",
            "lhConfig": self.env.tally_config,
            "zdConfig": "",
            "realShift": "1",
            "sheetNo": "",
            "taskId": self.env.dst_id_de,
            "shift": self.env.shift,
            "location": self.env.ygc_id,
            "dynamicLoc": "",
            "pieces": self.env.gtpks,
            "pkgType": self.env.pktype,
            "opproc": opproc_de,
            "ptNum": float(self.env.gtwg) / float(self.env.gtpks),
            "weight": self.env.gtwg,
            "volumn": self.env.gtvol,
            "remark": "车进汇报-备注",
            "direction": "0",
            "cover": "N",
            "danger": "N",
            "largeSized": "N",
            "_XID": "row_5911",
            "plgId": self.env.plg_id
        }
        res = self.request_main("POST", "/tos/wms/tally/delivery/report", json=payload)
        data = res.json()
        if check.equal(int(data["status"]), 200):
            self.env.goa_id_de = \
                self.db.select_from_table("select goa_id "
                                          "from wms_goods_occupy_activities "
                                          "where goa_dst_id = '{dst_id}'"
                                          .format(dst_id=self.env.dst_id_de)).loc[0, 'goa_id']
        else:
            self.logger.error("新增进货汇报失败")

    def delete_tally_report(self, task_type):
        goa_id = self.env.goa_id_de if task_type == 'de' else self.env.goa_id_ld
        payload = [goa_id]
        res = self.request_main("POST", "/tos/wms/WmsGoodsOccupsActivities/remove", json=payload)
        data = res.json()
        check.equal(int(data["status"]), 200)

    def tally_report_audit(self, task_type):
        goa_id = self.env.goa_id_de if task_type == 'de' else self.env.goa_id_ld
        payload = {"goaAduitFlag": "Y"}
        res = self.request_main("PUT", "/tos/wms/WmsGoodsOccupsActivities/task/audit/status/{goa_id}"
                                .format(goa_id=goa_id), params=payload)
        data = res.json()
        check.equal(int(data["status"]), 200)

    def tally_report_audit_cancel(self, task_type):
        goa_id = self.env.goa_id_de if task_type == 'de' else self.env.goa_id_ld
        payload = {"goaAduitFlag": "N"}
        res = self.request_main("PUT", "/tos/wms/WmsGoodsOccupsActivities/task/audit/status/{goa_id}"
                                .format(goa_id=goa_id), params=payload)
        data = res.json()
        check.equal(int(data["status"]), 200)

    def de_task_audit(self):
        self.env.tad_stt = self.cus.get_datetime_add(self.env.dst_opdate, day=-1, hour=18)
        self.env.tad_edt = self.cus.get_datetime_add(self.env.dst_opdate, hour=7)
        payload = {
            "staPiles": "N",
            "staPallet": 0,
            "staPulp": 0,
            "staRemark": "",
            "shiftTaskAuditDetailEntityList": [
                {
                    "tadGtypecd": self.env.gtypecd,
                    "tadCargoNm": self.env.gname,
                    "tadStartTime": self.env.tad_stt,
                    "tadEndTime": self.env.tad_edt,
                    "_XID": "row_2535"
                }
            ],
            "staDstId": self.env.dst_id_de
        }
        res = self.request_main("POST", "/tos/dts/shiftTaskAudit", json=payload)
        data = res.json()
        check.equal(int(data["status"]), 200)

    def task_audit_cancel(self, task_type):
        dst_id = self.env.dst_id_de if task_type == 'de' else self.env.dst_id_ld
        payload = {"dstId": dst_id}
        res = self.request_main("PUT", "/tos/dts/shiftTaskAudit/cancel", params=payload)
        data = res.json()
        check.equal(int(data["status"]), 200)

    def worksheet_wk_generate(self, task_type):
        dst_id = self.env.dst_id_de if task_type == 'de' else self.env.dst_id_ld
        if task_type == 'de':
            self.env.pws_id_de = \
                self.db.select_from_table("select pws_id "
                                          "from pws_work_sheet "
                                          "where pws_dts_id = '{dst_id}'"
                                          .format(dst_id=dst_id)).loc[0, 'pws_id']
        else:
            self.env.pws_id_ld = \
                self.db.select_from_table("select pws_id "
                                          "from pws_work_sheet "
                                          "where pws_dts_id = '{dst_id}'"
                                          .format(dst_id=dst_id)).loc[0, 'pws_id']
        pws_id = self.env.pws_id_de if task_type == 'de' else self.env.pws_id_ld
        res = self.request_main("POST", "/tos/pws/workSheetWk/gen/{pws_id}".format(pws_id=pws_id))
        data = res.json()
        check.equal(int(data["status"]), 200)

    def worksheet_machine_generate(self, task_type):
        pws_id = self.env.pws_id_de if task_type == 'de' else self.env.pws_id_ld
        res = self.request_main("POST", "/tos/pws/workSheetMachine/gen/{pws_id}".format(pws_id=pws_id))
        data = res.json()
        check.equal(int(data["status"]), 200)

    def worksheet_delete(self, task_type):
        pws_id = self.env.pws_id_de if task_type == 'de' else self.env.pws_id_ld
        if task_type == 'de':
            self.env.wsw_id_de = \
                self.db.select_from_table("select wsw_id "
                                          "from pws_work_sheet_wk "
                                          "where wsw_pws_id = '{pws_id}'"
                                          .format(pws_id=pws_id)).loc[0, 'wsw_id']
        else:
            self.env.wsw_id_ld = \
                self.db.select_from_table("select wsw_id "
                                          "from pws_work_sheet_wk "
                                          "where wsw_pws_id = '{pws_id}'"
                                          .format(pws_id=pws_id)).loc[0, 'wsw_id']
        wsw_id = self.env.wsw_id_de if task_type == 'de' else self.env.wsw_id_ld
        res = self.request_main("DELETE", "/tos/pws/workSheetWk/{wsw_id}".format(wsw_id=wsw_id))
        data = res.json()
        check.equal(int(data["status"]), 200)

    def worksheet_control_audit(self, task_type):
        pws_id = self.env.pws_id_de if task_type == 'de' else self.env.pws_id_ld
        payload = {
            "pwsId": pws_id,
            "pwsProdAuditTag": "Y"
        }
        res = self.request_main("PUT", "/tos/pws/workSheet/examine", json=payload)
        data = res.json()
        check.equal(int(data["status"]), 200)

    def worksheet_control_audit_cancel(self, task_type):
        pws_id = self.env.pws_id_de if task_type == 'de' else self.env.pws_id_ld
        payload = {
            "pwsId": pws_id,
            "pwsProdAuditTag": "N"
        }
        res = self.request_main("PUT", "/tos/pws/workSheet/examine", json=payload)
        data = res.json()
        check.equal(int(data["status"]), 200)

    def worksheet_hr_audit(self, task_type):
        pws_id = self.env.pws_id_de if task_type == 'de' else self.env.pws_id_ld
        payload = {
            "pwsId": pws_id,
            "pwsHrAuditTag": "Y"
        }
        res = self.request_main("PUT", "/tos/pws/workSheet/examine", json=payload)
        data = res.json()
        check.equal(int(data["status"]), 200)

    def worksheet_hr_audit_cancel(self, task_type):
        pws_id = self.env.pws_id_de if task_type == 'de' else self.env.pws_id_ld
        payload = {
            "pwsId": pws_id,
            "pwsHrAuditTag": "N"
        }
        res = self.request_main("PUT", "/tos/pws/workSheet/examine", json=payload)
        data = res.json()
        check.equal(int(data["status"]), 200)

    def run(self):
        self.set_values()
        self.get_user()
        self.add_schedule()
        self.confirm_report()
        self.subarea()
        self.add_berth_plan()
        self.add_accept_w()
        self.add_warehouse_plan()
        self.add_shift_task_de()
        self.tally_attend()
        self.tally_arrange('de')
        self.workgroup_arrange('de')
        self.add_stack_prerecording()
        self.in_door_check()
        self.add_stack_prerecording()
        self.in_door_check()
        self.in_door_pass()
        self.tally_report_de('W')
        self.out_door_pass()
        self.tally_report_audit('de')
        self.de_task_audit()
        self.worksheet_wk_generate('de')
        self.worksheet_machine_generate('de')
        self.worksheet_control_audit('de')
        self.worksheet_hr_audit('de')

    def rollback(self):
        self.worksheet_hr_audit_cancel('de')
        self.worksheet_control_audit_cancel('de')
        self.worksheet_delete('de')
        self.task_audit_cancel('de')
        self.tally_report_audit_cancel('de')
        self.delete_tally_report('de')
        self.workgroup_arrange_delete('de')
        self.tally_arrange_remove('de')
        self.tally_attend_cancel()
        self.delete_shift_task('de')
        self.delete_warehouse_plan()
        self.delete_accept()
        # self.subarea_cancel()
        # self.confirm_report_cancel()
        # self.delete_schedule()


def get_token():
    payload = {
        "little_girl": "ljadmin",
        "little_boy": "q1234567",
        "verification": "xxx"
    }
    headers = {'Content-Type': 'application/json'}
    r = RequestMain("10.166.0.131:20000", headers)
    res = r.request_main("POST", "/auth/saas/authorization/login/simple", headers=headers, json=payload)
    return json.loads(res.text)["data"]["access_token"]


if __name__ == '__main__':
    h1 = "10.166.0.131:20000"
    h2 = {
        'Content-Type': 'application/json',
        "Authorization": 'Bearer ' + get_token()
    }
    a = DeliverW(h1, h2)
    a.run()
