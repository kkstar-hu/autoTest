# -*- coding:utf-8 -*-
# Developer         : baishijun
# Development Time  : 2023/5/15 9:15
# Document Name     : ship_w.py.PY
# Development Tool  : PyCharm


import json
import random
from pytest_check import check
from BTOSLJ.Controls.BTOS_requests import RequestMain
from BTOSLJ.Controls.BTOS_db import GetPg
from BTOSLJ.Controls.BTOS_data import BtosTempData, BtosCustomData
import os


class ShipW(RequestMain):

    def __init__(self, host, header):
        super().__init__(host, header)
        self.env = BtosTempData(os.path.join(os.path.dirname(__file__) + r"\Excel\test_env_e_w.yaml"))
        self.cus = BtosCustomData()
        self.db = GetPg("10.166.0.137")

    def add_bill(self):
        payload = {
            "bilVoyId": self.env.voy_id,
            "bilBillNbr": self.env.bill_no,
            "bilTermcd": self.env.term_cd,
            "bilBillTrade": self.env.trade_type,
            "bilAgentId": self.env.agent_id,
            "bilOwnerId": self.env.owner_id,
            "bilTradeTerms": "3",
            "bilRemark": "外贸出口舱单备注",
            "bilProperty": "0",
            "bilBillIefg": self.env.iefg,
            "bilBillType": "B",
            "bilDirect": self.env.flow_direct,
            "bilDischargePort": "",
            "bilLetpass": "Y",
            "bilPass": "Y",
            "bilTradeType": "",
            "bilChkType": "",
            "bilCollig": "",
            "busGoodsEntities": [
                {
                    "gdsMarkno": self.env.mark_no,
                    "gdsGname": self.env.gname,
                    "gdsGtpks": self.env.gtpks,
                    "gdsGtwg": self.env.gtwg,
                    "bpgPkgCode": [self.env.pktype],
                    "gdsGtvol": self.env.gtvol,
                    "gdsGlength": 0,
                    "gdsGheight": 0,
                    "gdsGwidth": 0,
                    "gdsGtypecd": self.env.gtypecd,
                    "gdsDngCode": "",
                    "sjGtpks": "",
                    "sjGtwg": "",
                    "sjGtvol": "",
                    "pkTypes": [],
                    "PktypeList": [],
                    "goodsPackagesEntityList": [
                        {
                            "bpgPkgCode": self.env.pktype
                        }
                    ]
                }
            ],
            "gdsIds": []
        }
        res = self.request_main("POST", "/tos/wms/bills", json=payload)
        data = res.json()
        if check.equal(int(data["status"]), 200):
            self.env.bil_id = data["data"]["bilId"]
        else:
            self.logger.error("新增外贸出口舱单失败")

    def delete_bill(self):
        res = self.request_main("DELETE", "/tos/wms/bills/{bil_id}".format(bil_id=self.env.bil_id))
        data = res.json()
        check.equal(int(data["status"]), 200)

    def allocat_goods(self):
        self.env.ygt_id = \
            self.db.select_from_table("select goa_ygt_id from wms_goods_occupy_activities "
                                      "where goa_id='{goa_id}'"
                                      .format(goa_id=self.env.goa_id_de)).loc[0, 'goa_ygt_id']
        self.env.gds_id = \
            self.db.select_from_table("select gds_id from bus_goods "
                                      "where gds_bil_id='{bil_id}'"
                                      .format(bil_id=self.env.bil_id)).loc[0, 'gds_id']
        payload = {
            "gdsId": self.env.gds_id,
            "voyId": self.env.voy_id,
            "goods": [
                {
                    "ygtGtpks": self.env.gtpks,
                    "ygtGtvol": self.env.gtvol,
                    "ygtGtwg": self.env.gtwg,
                    "ygtId": self.env.ygt_id
                }
            ]
        }
        res = self.request_main("POST", "/tos/wms/allocatedGoods/allocate", json=payload)
        data = res.json()
        if check.equal(int(data["status"]), 200):
            self.env.bag_id = \
                self.db.select_from_table("select bag_id from bus_allocated_goods "
                                          "where bag_gds_id='{gds_id}'"
                                          .format(gds_id=self.env.gds_id)).loc[0, 'bag_id']
        else:
            self.logger.error("舱单配货失败")

    def allocat_goods_cancel(self):
        payload = [self.env.bag_id]
        res = self.request_main("POST", "/tos/wms/allocatedGoods/cancel", json=payload)
        data = res.json()
        check.equal(int(data["status"]), 200)

    def add_vessel_plan(self):
        self.env.dvp_opsttm = self.cus.get_datetime_add(self.env.vbt_pbthdt, minute=30)
        self.env.dvp_opedtm = self.cus.get_datetime_add(self.env.dvp_opsttm, day=1)
        self.env.dvp_opdate = self.cus.to_date(self.cus.get_datetime_add(self.env.vbt_pbthdt, day=-1))
        payload = {
            "dvpTrade": self.env.trade_type,
            "dvpBerthNo": "{},{}".format(self.env.bth_no, self.env.bth_no),
            "dvpCargo": self.env.gtypecd,
            "dvpTermcd": self.env.term_cd,
            "dvpOpsttm": self.env.dvp_opsttm,
            "dvpOpedtm": self.env.dvp_opedtm,
            "dvpVoyId": self.env.voy_id,
            "dvpScdId": self.env.scd_id,
            "dvpVoyage": self.env.voyage,
            "dvpVslCode": self.env.vsl_cd,
            "dvpIefg": self.env.iefg,
            "dvpWgtTotal": self.env.gtwg,
            "dvpThisLeft": self.env.gtwg,
            "dvpTurnTon": "0",
            "dvpShipGroup": "",
            "dvpRemark": "装船-大船作业计划备注",
            "dtsVesselRouteEntityList": [
                {
                    "dvrShiftNo": "1",
                    "pscOrder": 0,
                    "shiftName": "夜班",
                    "dvrRouteNum": "1",
                    "dvrOpton": "",
                    "dvrKeyRoute": "N",
                    "dvrGtpks": "",
                    "dvrCrewNum": "",
                    "dvrThroughput": self.env.gtwg,
                    "dvrOpproc": self.env.opproc_ld,
                    "dvrCraft": self.env.craft_ld,
                    "dvrTermcd": self.env.term_cd,
                    "dtsRouteWkgroupEntityList": [
                        {
                            "contentShow": True,
                            "drwDeptId": "b20000daceb342798d22d4499077647d",
                            "drwWorkerNum": "5"
                        }
                    ],
                    "dtsRouteMachinesEntityList": [
                        {
                            "contentShow": True,
                            "drmMacType": "9",
                            "drmDeptId": "e1c7a9d9bcba4be1b33f149fce9b422c",
                            "drmMacNum": "2",
                            "drmRemark": None
                        }
                    ]
                },
                {
                    "dvrShiftNo": "2",
                    "pscOrder": 1,
                    "shiftName": "日班",
                    "dvrRouteNum": "0",
                    "dvrOpton": "",
                    "dvrKeyRoute": "N",
                    "dvrGtpks": "",
                    "dvrCrewNum": "",
                    "dvrThroughput": "0",
                    "dvrOpproc": "",
                    "dvrCraft": "",
                    "dvrTermcd": self.env.term_cd,
                    "dtsRouteWkgroupEntityList": [],
                    "dtsRouteMachinesEntityList": []
                }
            ],
            "dvpOpdate": self.env.dvp_opdate,
            "dvrIds": []
        }
        res = self.request_main("POST", "/tos/dts/vesselPlan", json=payload)
        data = res.json()
        if check.equal(int(data["status"]), 200):
            self.env.dvp_id = data["data"]["dvpId"]
            self.env.route_id_ld = data["data"]["dtsVesselRouteEntityList"][0]["dtsRouteMachinesEntityList"][0][
                "drmRouteId"]
        else:
            self.logger.error("新增大船作业计划失败")

    def delete_vessel_plan(self):
        res = self.request_main("DELETE", "/tos/dts/vesselPlan/{dvp_id}".format(dvp_id=self.env.dvp_id))
        data = res.json()
        check.equal(int(data["status"]), 200)

    def add_shift_task_ld(self):
        payload = {
            "dtsShiftTaskEntities": [
                {
                    "dstRouteId": self.env.route_id_ld,
                    "dstTaskType": 'V',
                    "dstOpdate": self.env.dst_opdate,
                    "dstShiftCode": self.env.shift,
                    "dstOpproc": self.env.opproc_ld,
                    "dstBerthno": "{},{}".format(self.env.bth_no, self.env.bth_no),
                    "dstCraft": self.env.craft_ld,
                    "dstOptype": self.env.optype_ld,
                    "dstPWgt": self.env.gtwg,
                    "dstAWgt": 0,
                    "dstHatchNo": '01,111',
                    "dstHatchList": [],
                    "dstCargo": self.env.gtypecd,
                    "dstPktype": self.env.pktype,
                    "dstPmGroup": "",
                    "dstYardNote": "",
                    "dstSecurityNote": "",
                    "dstRemark": "装船-大船作业计划备注|当班任务备注",
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
                    "shiftTaskMactypeEntities": [
                        {
                            "stmMacType": "9",
                            "stmMacNum": 2,
                            "stmPosType": "LJQD",
                            "stmPricingMode": "1",
                            "stmDeptId": "e1c7a9d9bcba4be1b33f149fce9b422c",
                            "stmMileage": "",
                            "stmRemark": None
                        }
                    ],
                    "stmIds": [],
                    "shiftTaskWkgroupEntities": [
                        {
                            "stwWorkerNum": 5,
                            "stwGroup": "",
                            "stwPosType": "LJQD",
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
            self.env.dst_id_ld = data["data"][0]["dstId"]
            self.env.stw_id_ld = data["data"][0]["shiftTaskWkgroupEntities"][0]["stwId"]
            self.env.stm_id_ld = data["data"][0]["shiftTaskMactypeEntities"][0]["stmId"]
        else:
            self.logger.error("新增装船任务失败")

    def machine_attend(self):
        payload = {
            "dtsYardWorkingMachinesEntities": [
                {
                    "ymaOpdate": self.env.dst_opdate,
                    "ymaShift": self.env.shift,
                    "ymaYmcId": "34554326c8da5344006e281755fee32b",
                    "ymaDeptId": "e1c7a9d9bcba4be1b33f149fce9b422c",
                    "ymaDeptName": "机械运行部",
                    "ymaMachinesType": "9",
                    "ymaMachinesTypeName": "门机",
                    "ymaMachinesNo": "4001",
                    "dtsYardWorkingDriverEntityList": []
                }
            ],
            "dywmIds": []
        }
        res = self.request_main("POST", "/tos/dts/yardWorkingMachines/stored", json=payload)
        data = res.json()
        if check.equal(int(data["status"]), 200):
            # 机械出勤id
            self.env.yma_id = \
                self.db.select_from_table("select yma_id "
                                          "from dts_yard_working_machines yma "
                                          "join pub_yard_machines ymc on yma.yma_ymc_id=ymc.ymc_id "
                                          "where yma_opdate='{optype}' and yma_shift='{shift}'"
                                          " and ymc.ymc_mchno='{machine_no}' "
                                          .format(optype=self.env.dst_opdate, shift=self.env.shift,
                                                  machine_no='4001')).loc[0, 'yma_id']
        else:
            self.logger.error("机械出勤失败")

    def machine_attend_cancel(self):
        payload = {
            "dtsYardWorkingMachinesEntities": [],
            "dywmIds": [self.env.yma_id]
        }
        res = self.request_main("POST", "/tos/dts/yardWorkingMachines/stored", json=payload)
        data = res.json()
        check.equal(int(data["status"]), 200)

    def driver_arrange(self):
        payload = {
            "dtsYardWorkingMachinesEntities": [
                {
                    "ymaId": self.env.yma_id,
                    "ymaOpdate": self.env.dst_opdate,
                    "ymaShift": self.env.shift,
                    "ymaYmcId": "34554326c8da5344006e281755fee32b",
                    "ymaDeptId": "e1c7a9d9bcba4be1b33f149fce9b422c",
                    "ymaDeptName": "机械运行部",
                    "ymaMachinesType": "9",
                    "ymaMachinesTypeName": "门机",
                    "ymaMachinesNo": "4001",
                    "dtsYardWorkingDriverEntityList": [
                        {
                            "ydrDriver": "13647368bb514aec80a10c41881e1f4e",
                            "ydrRoleCode": "",
                            "ydrOvertime": "N"
                        }
                    ]
                }
            ],
            "dywdIds": []
        }
        res = self.request_main("POST", "/tos/dts/yardWorkingMachines/stored", json=payload)
        data = res.json()
        check.equal(int(data["status"]), 200)

    def driver_arrange_delete(self):
        # 司机出勤id
        self.env.ydr_id = \
            self.db.select_from_table("select ydr_id "
                                      "from dts_yard_working_driver "
                                      "where ydr_yma_id = '{yma_id}'"
                                      .format(yma_id=self.env.yma_id)).loc[0, 'ydr_id']
        payload = {
            "dywdIds": [self.env.ydr_id]
        }
        res = self.request_main("DELETE", "/tos/dts/yardWorkingMachines/cutoffDirver", json=payload)
        data = res.json()
        check.equal(int(data["status"]), 200)

    def machine_arrange(self):
        self.env.dmc_sttm = self.cus.get_datetime_add(self.env.dst_opdate, day=-1, hour=18)
        self.env.dmc_edtm = self.cus.get_datetime_add(self.env.dst_opdate, hour=6)
        self.env.instructor_config = \
            self.db.select_from_table("select stc_id "
                                      "from dts_shift_task_config "
                                      "where stc_dts_id='{dst_id}' and stc_type='2'"
                                      .format(dst_id=self.env.dst_id_ld)).loc[0, 'stc_id']
        payload = {
            "configId": self.env.instructor_config,
            "machines": [
                {
                    "drivers": [],
                    "dmcDstId": self.env.dst_id_ld,
                    "dmcYmaId": self.env.yma_id,
                    "dmcYmcId": "34554326c8da5344006e281755fee32b",
                    "dmcYmcNo": "4001",
                    "dmcMacType": "9",
                    "dmcMacNm": "门机",
                    "dmcDeptId": "e1c7a9d9bcba4be1b33f149fce9b422c",
                    "dmcPosType": "LJQD",
                    "dmcPosNm": "罗泾起点",
                    "dmcSttm": self.env.dmc_sttm,
                    "dmcEdtm": self.env.dmc_edtm,
                    "dmcLoad": "",
                    "dmcRemark": "",
                    "_XID": "row_5646"
                }
            ]
        }
        res = self.request_main("POST", "/tos/dts/shiftTaskConfig/{instructor_config}/report"
                                .format(instructor_config=self.env.instructor_config),
                                json=payload)
        data = res.json()
        check.equal(int(data["status"]), 200)

    def machine_diver_match(self):
        payload = {
            "stcId": self.env.instructor_config
        }
        res = self.request_main("POST", "/tos/dts/shiftTaskConfig/match", params=payload)
        data = res.json()
        check.equal(int(data["status"]), 200)

    def machine_arrange_remove(self):
        self.env.cma_id = \
            self.db.select_from_table("select cma_id "
                                      "from dts_shift_task_config_machine "
                                      "where cma_stc_id = '{instructor_config}'"
                                      .format(instructor_config=self.env.instructor_config)).loc[0, 'cma_id']
        payload = [self.env.cma_id]
        res = self.request_main("DELETE", "/tos/dts/shiftTaskConfigMachine/remove", json=payload)
        data = res.json()
        check.equal(int(data["status"]), 200)

    def machine_arrange_delete(self):
        # 机械安排id
        self.env.dmc_id = \
            self.db.select_from_table("select dmc_id "
                                      "from dts_shift_task_machines "
                                      "where dmc_dst_id = '{dst_id}'"
                                      .format(dst_id=self.env.dst_id_ld)).loc[0, 'dmc_id']
        payload = {
            "dmcIds": [self.env.dmc_id],
            "stoIds": [],
            "dmcDstId": self.env.dst_id_ld
        }
        res = self.request_main("DELETE", "/tos/dts/shiftTaskMachines/deleteMachines", json=payload)
        data = res.json()
        check.equal(int(data["status"]), 200)

    def warehouse_arrange(self):
        payload = {
            "dtsShiftTaskOccupyList": [
                {
                    "stoDtsId": self.env.dst_id_ld,
                    "stoYgcId": self.env.ygc_id,
                    "stoYgcNm": self.env.ygc_no,
                    "stoIeflag": 2,
                    "stoRemark": "库场安排-备注",
                    "createUser": None,
                    "createTime": None,
                    "updateUser": None,
                    "updateTime": None,
                    "_XID": "row_2087"
                }
            ]
        }
        res = self.request_main("POST", "/tos/dts/shiftTaskOccupy", json=payload)
        data = res.json()
        if check.equal(int(data["status"]), 200):
            self.env.sto_id = data["data"]["dtsShiftTaskOccupyList"][0]["stoId"]
        else:
            self.logger.error("库场安排失败")

    def warehouse_arrange_cancel(self):
        payload = {
            "stoIds": [self.env.sto_id]
        }
        res = self.request_main("DELETE", "/tos/dts/shiftTaskOccupy/deleteOccupy", json=payload)
        data = res.json()
        check.equal(int(data["status"]), 200)

    def berth(self):
        self.env.vbt_id = \
            self.db.select_from_table("select vbt_id "
                                      "from bps_vessel_berthes "
                                      "where vbt_scd_id = '{scd_id}'"
                                      .format(scd_id=self.env.scd_id)).loc[0, 'vbt_id']
        payload = {
            "vbtScdId": self.env.scd_id,
            "vbtStatus": "1",
            "vbtTermcd": self.env.term_cd,
            "vbtAstpst": self.env.bth_startpst,
            "vbtAedpst": self.env.bth_startpst + self.env.vsl_loa,
            "vbtAbthdirect": "L",
            "vbtBthAbthno": "{},{}".format(self.env.bth_no, self.env.bth_no),
            "vbtBthAbthnost": self.env.bth_no,
            "vbtBthAbthnoed": self.env.bth_no,
            "vbtAbthdt": self.cus.get_datetime_now,
            "vbtAbthdraft": 20,
            "vbtAfrom": "",
            "vbtAdptdt": "",
            "vbtAdptdraft": "0",
            "vbtAto": "",
            "actualBowPiles": [],
            "actualSternPiles": [],
            "vbtIandeGear": "",
            "vbtId": self.env.vbt_id,
            "vbbIds": "",
            "scdRStartTime": self.env.dvp_opsttm,
            "scdREndTime": self.env.dvp_opedtm,
            "vbbIdPlan": [],
            "vbbIdActual": []
        }
        res = self.request_main("POST", "/tos/bps/vesselBerthes/updateVesselBerthes", json=payload)
        data = res.json()
        check.equal(int(data["status"]), 200)

    def tally_report_ld(self):
        self.env.barcode_ld = \
            self.db.select_from_table("select gds_bar_code "
                                      "from bus_goods "
                                      "where gds_bil_id = '{bil_id}' "
                                      .format(bil_id=self.env.bil_id)).loc[0, 'gds_bar_code']
        payload = {
            "barCode": self.env.barcode_ld,
            "planNo": "",
            "billNo": self.env.bill_no,
            "length": "0",
            "width": "0",
            "height": "0",
            "empId": self.env.user_id,
            "markNo": self.env.mark_no,
            "gateId": "",
            "truckNo": "",
            "flatCarNo": "",
            "cargoKind": self.env.gtypecd,
            "contractNo": self.env.ht_no,
            "pieceNo": "",
            "pieceCode": "",
            "damage": "0",
            "cntrNo": "",
            "wbFlag": "N",
            "realMarkno": "N",
            "specs": "",
            "transHatchNo": "",
            "lhConfig": "",
            "zdConfig": self.env.instructor_config,
            "realShift": "1",
            "sheetNo": "",
            "bagId": self.env.bag_id,
            "taskId": self.env.dst_id_ld,
            "shift": self.env.shift,
            "location": self.env.ygc_id,
            "dynamicLoc": self.env.dynamic_loc,
            "hatchNo": "01",
            "pieces": self.env.gtpks,
            "pkgType": self.env.pktype,
            "opproc": self.env.opproc_ld,
            "ptNum": float(self.env.gtwg) / float(self.env.gtpks),
            "weight": self.env.gtwg,
            "volumn": self.env.gtvol,
            "remark": "装船汇报-备注",
            "direction": "0",
            "cover": "N",
            "danger": "N",
            "largeSized": "N",
            "_XID": "row_5911",
            "voyId": self.env.voy_id,
            "gdsId": self.env.gds_id
        }
        res = self.request_main("POST", "/tos/wms/tally/load/report", json=payload)
        data = res.json()
        if check.equal(int(data["status"]), 200):
            self.env.goa_id_ld = \
                self.db.select_from_table("select goa_id "
                                          "from wms_goods_occupy_activities "
                                          "where goa_dst_id = '{dst_id}'"
                                          .format(dst_id=self.env.dst_id_ld)).loc[0, 'goa_id']
        else:
            self.logger.error("新增装船汇报失败")

    def ld_task_audit(self):
        payload = {
            "staPiles": "N",
            "staPallet": 0,
            "staPulp": 0,
            "staRemark": "",
            "staDstId": self.env.dst_id_ld
        }
        res = self.request_main("POST", "/tos/dts/shiftTaskAudit", json=payload)
        data = res.json()
        check.equal(int(data["status"]), 200)

    def unberth(self):
        payload = {
            "vbtStatus": "2",
            "vbtScdId": self.env.scd_id,
            "vbtId": self.env.vbt_id,
            "vbtAdptdt": self.env.vbt_pdptdt,
            "vbtAto": "",
            "vbtAdptdraft": "20",
            "vbtAbthdt": self.env.vbt_pbthdt,
            "vbtAbthdraft": 20,
            "vbtAedpst": 1203,
            "vbtAstpst": 1053.46,
            "scdRStartTime": self.env.dvp_opsttm,
            "scdREndTime": self.env.dvp_opedtm,
            "departureFlag": "Y",
            "modifyFlag": "N"
        }
        res = self.request_main("POST", "/tos/bps/vesselBerthes/updateVesselBerthes", json=payload)
        data = res.json()
        check.equal(int(data["status"]), 200)




