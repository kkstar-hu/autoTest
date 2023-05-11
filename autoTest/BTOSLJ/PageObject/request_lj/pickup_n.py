# -*- coding:utf-8 -*-
# Developer         : baishijun
# Development Time  : 2023/5/6 11:07
# Document Name     : pickup_n.PY
# Development Tool  : PyCharm

import json
from pytest_check import check
from BTOSLJ.Controls.BTOS_requests import ExcelHandler, RequestMain
from BTOSLJ.Controls.BTOS_db import GetPg
from BTOSLJ.Controls.BTOS_data import BtosTempData, BtosCustomData
import os


class PickupN(RequestMain):

    def __init__(self, host, header):
        super().__init__(host, header)
        self.env = BtosTempData(os.path.join(os.path.dirname(__file__) + r"\Excel\test_env_i_n.yaml"))
        self.handler = ExcelHandler(os.path.join(os.path.dirname(__file__) + r"\Excel\mainflow.xlsx"))
        self.sheet = self.handler.read_sheet("卸船提货")
        self.cus = BtosCustomData()
        self.db = GetPg("10.166.0.137")

    def add_accept(self):
        s = self.sheet[45]
        self.env.pln_opsttm = self.cus.get_datetime_add(self.env.dst_opdate, hour=18)
        self.env.pln_opedtm = self.cus.get_datetime_add(self.env.dst_opdate, day=1, hour=18)
        self.env.payer_tel = self.cus.get_phone
        self.env.fleet_tel = self.cus.get_phone
        payload = json.loads(s["payload"])
        payload["plnTrade"] = self.env.trade_type
        payload["plnIefg"] = self.env.iefg
        payload["plnTermcd"] = self.env.term_cd
        payload["plnVoyId"] = self.env.voy_id
        payload["plnOpsttm"] = self.env.pln_opsttm
        payload["plnOpedtm"] = self.env.pln_opedtm
        payload["operationProcess"] = [self.env.opproc_pk]
        payload["plnTransmode"] = self.env.optype_pk
        payload["plnGtpks"] = self.env.gtpks
        payload["plnGtwg"] = self.env.gtwg
        payload["pasPlansExtendEntity"]["ppePayerTel1"] = self.env.payer_tel
        payload["pasPlansExtendEntity"]["ppePayerTel2"] = self.env.payer_tel
        payload["pasPlansExtendEntity"]["ppeFleetTel"] = self.env.fleet_tel
        payload["pasPlanGoodsEntities"][0]["plgBillno"] = self.env.bill_no
        payload["pasPlanGoodsEntities"][0]["plgMarkerno"] = self.env.mark_no
        payload["pasPlanGoodsEntities"][0]["plgGname"] = self.env.gname
        payload["pasPlanGoodsEntities"][0]["plgPGtwg"] = self.env.gtwg
        payload["pasPlanGoodsEntities"][0]["plgPGtpks"] = self.env.gtpks
        payload["pasPlanGoodsEntities"][0]["plgPGtvol"] = self.env.gtvol
        payload["pasPlanGoodsEntities"][0]["plgPktype"] = self.env.pktype
        payload["pasPlanGoodsEntities"][0]["plgSttm"] = self.env.pln_opsttm
        payload["pasPlanGoodsEntities"][0]["plgEdtm"] = self.env.pln_opedtm
        payload["pasPlanGoodsEntities"][0]["plgCargoRemark"] = self.env.ygc_no
        payload["pasPlanGoodsEntities"][0]["plgGtypecd"] = self.env.gtypecd
        payload["pasPlanGoodsEntities"][0]["plgVoyId"] = self.env.voy_id
        payload["pasPlanGoodsEntities"][0]["plgGdsId"] = self.env.gds_id
        payload["pasPlanGoodsEntities"][0]["plgPkName"] = self.env.pkname
        res = self.request_main(s["method"], s["path"], json=payload)
        data = res.json()
        if check.equal(int(data["status"]), int(s["expected_res"])):
            self.env.pln_id = data["data"]["plnId"]
            self.env.pln_no = data["data"]["plnPlanno"]
            self.env.plg_id = \
                self.db.select_from_table("select plg_id "
                                          "from pas_plan_goods "
                                          "where plg_pln_id='{pln_id}' "
                                          .format(pln_id=self.env.pln_id)).loc[0, 'plg_id']
        else:
            self.logger.error("新增提货受理失败")

    def delete_accept(self):
        s = self.sheet[46]
        res = self.request_main(s["method"], s["path"].format(pln_id=self.env.pln_id))
        data = res.json()
        check.equal(int(data["status"]), int(s["expected_res"]))

    def add_warehouse_plan(self):
        s = self.sheet[47]
        payload = json.loads(s["payload"])
        payload["dwpPlnId"] = self.env.pln_id
        payload["dwpPlanno"] = self.env.pln_no
        payload["dwpOpsttm"] = self.env.dvp_opdate
        payload["dwpOpedtm"] = self.env.pln_opsttm
        payload["dwpTermcd"] = self.env.term_cd
        payload["plnOpproc"] = self.env.opproc_pk
        payload["plnTransmode"] = self.env.optype_pk
        payload["dtsWarehouseRouteEntityList"][1]["dwrOpton"] = self.env.gtwg
        payload["dtsWarehouseRouteEntityList"][1]["dwrOpproc"] = self.env.opproc_pk
        res = self.request_main(s["method"], s["path"], json=payload)
        data = res.json()
        if check.equal(int(data["status"]), int(s["expected_res"])):
            self.env.dwp_id = data["data"]["dwpId"]
            self.env.pk_route_id = data["data"]["dtsWarehouseRouteEntityList"][1]["dwrId"]
        else:
            self.logger.error("新增车驳作业计划失败")

    def delete_warehouse_plan(self):
        s = self.sheet[48]
        res = self.request_main(s["method"], s["path"].format(dwp_id=self.env.dwp_id))
        data = res.json()
        check.equal(int(data["status"]), int(s["expected_res"]))

    def add_shift_task_pk(self):
        s = self.sheet[49]
        self.env.dst_type_pk = 'W'
        payload = json.loads(s["payload"])
        payload["dtsShiftTaskEntities"][0]["dstRouteId"] = self.env.pk_route_id
        payload["dtsShiftTaskEntities"][0]["dstTaskType"] = self.env.dst_type_pk
        payload["dtsShiftTaskEntities"][0]["dstOpdate"] = self.env.dst_opdate
        payload["dtsShiftTaskEntities"][0]["dstShiftCode"] = self.env.shift
        payload["dtsShiftTaskEntities"][0]["dstOpproc"] = self.env.opproc_pk
        payload["dtsShiftTaskEntities"][0]["dstOptype"] = self.env.optype_pk
        payload["dtsShiftTaskEntities"][0]["dstPWgt"] = self.env.gtwg
        payload["dtsShiftTaskEntities"][0]["dstCargo"] = self.env.gtypecd
        payload["dtsShiftTaskEntities"][0]["dstPktype"] = self.env.pktype
        payload["dtsShiftTaskEntities"][0]["dstTermcd"] = self.env.term_cd
        res = self.request_main(s["method"], s["path"], json=payload)
        data = res.json()
        if check.equal(int(data["status"]), int(s["expected_res"])):
            self.env.pk_dst_id = data["data"][0]["dstId"]
            self.env.pk_stw_id = data["data"][0]["shiftTaskWkgroupEntities"][0]["stwId"]
        else:
            self.logger.error("新增提货当班任务失败")

    def warehouse_arrange(self):
        s = self.sheet[50]
        payload = json.loads(s["payload"])
        payload["dtsShiftTaskOccupyList"][0]["stoDtsId"] = self.env.pk_dst_id
        payload["dtsShiftTaskOccupyList"][0]["stoYgcId"] = self.env.ygc_id
        payload["dtsShiftTaskOccupyList"][0]["stoYgcNm"] = self.env.ygc_no
        res = self.request_main(s["method"], s["path"], json=payload)
        data = res.json()
        if check.equal(int(data["status"]), int(s["expected_res"])):
            self.env.sto_id = data["data"]["dtsShiftTaskOccupyList"][0]["stoId"]
        else:
            self.logger.error("库场安排失败")

    def warehouse_arrange_cancel(self):
        s = self.sheet[51]
        payload = json.loads(s["payload"])
        payload["stoIds"] = [self.env.sto_id]
        res = self.request_main(s["method"], s["path"], json=payload)
        data = res.json()
        check.equal(int(data["status"]), int(s["expected_res"]))

    def pk_tally_report(self):
        s = self.sheet[52]
        self.env.pk_barcode = \
            self.db.select_from_table("select plg_bar_code "
                                      "from pas_plan_goods "
                                      "where plg_id = '{plg_id}' "
                                      .format(plg_id=self.env.plg_id)).loc[0, 'plg_bar_code']
        self.env.truck_no = self.cus.get_license_plate
        payload = json.loads(s["payload"])
        payload["barCode"] = self.env.pk_barcode
        payload["planNo"] = self.env.pln_no
        payload["billNo"] = self.env.bill_no
        payload["markNo"] = self.env.mark_no
        payload["truckNo"] = self.env.truck_no
        payload["cargoKind"] = self.env.gtypecd
        payload["zdConfig"] = self.env.tally_config
        payload["taskId"] = self.env.pk_dst_id
        payload["shift"] = self.env.shift
        payload["location"] = self.env.ygc_id
        payload["dynamicLoc"] = self.env.little_loc
        payload["pieces"] = self.env.gtpks
        payload["pkgType"] = self.env.pktype
        payload["opproc"] = self.env.opproc_pk
        payload["ptNum"] = float(self.env.gtwg) / float(self.env.gtpks)
        payload["weight"] = self.env.gtwg
        payload["volumn"] = self.env.gtvol
        payload["voyId"] = self.env.voy_id
        payload["empId"] = self.env.user_id
        payload["plnId"] = self.env.pln_id
        payload["plgId"] = self.env.plg_id
        res = self.request_main(s["method"], s["path"], json=payload)
        data = res.json()
        if check.equal(int(data["status"]), int(s["expected_res"])):
            self.env.pk_goa_id = \
                self.db.select_from_table("select goa_id "
                                          "from wms_goods_occupy_activities "
                                          "where goa_dst_id = '{dst_id}'"
                                          .format(dst_id=self.env.pk_dst_id)).loc[0, 'goa_id']
        else:
            self.logger.error("新增提货汇报失败")

    def pk_task_audit(self):
        s = self.sheet[53]
        payload = json.loads(s["payload"])
        self.env.tad_stt = self.cus.get_datetime_add(self.env.dst_opdate, hour=7)
        self.env.tad_edt = self.cus.get_datetime_add(self.env.dst_opdate, hour=18)
        payload["staDstId"] = self.env.pk_dst_id
        payload["shiftTaskAuditDetailEntityList"][0]["tadGtypecd"] = self.env.gtypecd
        payload["shiftTaskAuditDetailEntityList"][0]["tadCargoNm"] = self.env.gname
        payload["shiftTaskAuditDetailEntityList"][0]["tadStartTime"] = self.env.tad_stt
        payload["shiftTaskAuditDetailEntityList"][0]["tadEndTime"] = self.env.tad_edt
        res = self.request_main(s["method"], s["path"], json=payload)
        data = res.json()
        check.equal(int(data["status"]), int(s["expected_res"]))

    def outdoor_pass(self):
        s = self.sheet[54]
        payload = json.loads(s["payload"])
        self.env.otr_id = \
            self.db.select_from_table("select otr_id "
                                      "from gts_outtruck_record "
                                      "where otr_truckno ='{truck_no}'"
                                      .format(truck_no=self.env.truck_no)).loc[0, 'otr_id']
        payload["otrId"] = self.env.otr_id
        res = self.request_main(s["method"], s["path"], json=payload)
        data = res.json()
        check.equal(int(data["status"]), int(s["expected_res"]))


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

'''
if __name__ == "__main__":
    host = "10.166.0.131:20000"
    header = {
        'Content-Type': 'application/json',
        "Authorization": 'Bearer ' + get_token()
    }

    a = PickupN(host, header)
    b = UnshipN(host, header)

    a.add_accept()
    a.add_warehouse_plan()
    a.add_shift_task_pk()
    b.tally_arrange('pk')
    b.workgroup_arrange('pk')
    a.warehouse_arrange()
    a.pk_tally_report()
    b.tally_report_audit('pk')
    a.pk_task_audit()
    a.outdoor_pass()
    b.worksheet_wk_generate('pk')
    b.worksheet_machine_generate('pk')
    b.worksheet_control_audit('pk')
    b.worksheet_hr_audit('pk')

    b.worksheet_hr_audit_cancel('pk')
    b.worksheet_control_audit_cancel('pk')
    b.task_audit_cancel('pk')
    b.tally_report_audit_cancel('pk')
    b.tally_report_delete('pk')
    a.warehouse_arrange_cancel()
    b.workgroup_arrange_delete('pk')
    b.tally_arrange_remove('pk')
    b.delete_shift_task('pk')
    a.delete_warehouse_plan()
    a.delete_accept()
'''