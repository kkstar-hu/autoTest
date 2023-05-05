import json
from pytest_check import check
import pytest
from BTOSLJ.Controls.BTOS_requests import ExcelHandler, RequestMain
from BTOSLJ.Controls.BTOS_db import GetPg
from BTOSLJ.Controls.BTOS_data import BtosTempData, BtosCustomData
import os


class UnshipN(RequestMain):

    def __init__(self, host, header):
        super().__init__(host, header)
        # print("实例对象创建: UnshipN", id(self))
        self.env = BtosTempData(os.path.join(os.path.dirname(__file__) + r"\Excel\test_env_i.txt"))
        self.handler = ExcelHandler(os.path.join(os.path.dirname(__file__) + r"\Excel\mainflow.xlsx"))
        self.sheet = self.handler.read_sheet("卸船")
        self.cus = BtosCustomData()
        self.db = GetPg("10.166.0.137")

    def set_values(self):
        gtypecd, pktype = self.cus.get_pktype
        self.env.gtypecd = gtypecd
        self.env.pktype = pktype
        self.env.voyage = self.cus.get_Ivoyage
        self.env.trade_type = 'N'
        self.env.gtwg = self.cus.get_gtwg
        self.env.gtpks = self.cus.get_gtpks
        self.env.gtvol = self.cus.get_gtvol
        self.env.iefg = 'I'
        self.env.shift = '2'
        self.env.opproc_dc = '014'  # 船=>场
        self.env.opprc_pk = '008'  # 场=>车
        self.env.ygc_no = 'A02/00'

    def add_vessel(self):
        s = self.sheet[0]
        res = self.request_main(method=s["method"], url=s["path"], json=json.loads(s["payload"]))
        data = res.json()
        if check.equal(int(data["status"]), int(s["expected_res"])):
            self.handler.write_sheet('卸船', s['case_id'] + 1, 8, data["status"])
            self.env.vsl_id = data["data"]["vslId"]
        '''
            if not check.any_failures():
                self.env.vsl_id = data["data"]["vslId"]
                self.handler.write_sheet('卸船', s['case_id'] + 1, 9, "Pass")
            else:
                self.handler.write_sheet('卸船', s['case_id'] + 1, 9, "Fail")
            '''

    def delete_vessel(self):
        s = self.sheet[1]
        res = self.request_main(s["method"], s["path"].format(vsl_id=self.env.vsl_id))
        data = res.json()
        check.equal(int(data["status"]), int(s["expected_res"]))

    def add_schedule(self):
        s = self.sheet[2]
        self.env.scd_eta = self.cus.get_datetime_now
        self.env.scd_etd = self.cus.get_datetime_add(self.env.scd_eta, day=2)
        payload = json.loads(s["payload"])
        payload["scdVslId"] = self.env.vsl_id
        payload["bpsIvoyageQuery"]["scdIvoyage"] = self.env.voyage
        payload["bpsIvoyageQuery"]["scdGoodsIlists"] = [self.env.gtypecd]
        payload["bpsIvoyageQuery"]["scdIton"] = self.env.gtwg
        payload["bpsIvoyageQuery"]["scdIvoyTrade"] = self.env.trade_type
        payload["scdEta"] = self.env.scd_eta
        payload["scdEtd"] = self.env.scd_etd
        payload["scdIton"] = self.env.gtwg
        res = self.request_main(s["method"], s["path"], json=payload)
        data = res.json()
        check.equal(int(data["status"]), int(s["expected_res"]))
        self.handler.write_sheet('卸船', s['case_id'] + 1, 8, data["status"])
        self.env.scd_id = data["data"]["scdId"]
        self.env.voy_id = \
            self.db.select_from_table("select voy_id from bps_voyage "
                                      "where voy_scd_id='{scd_id}' and voy_voyage='{voyage}' "
                                      .format(scd_id=self.env.scd_id, voyage=self.env.voyage)).loc[0, 'voy_id']

    def delete_schedule(self):
        s = self.sheet[3]
        res = self.request_main(s["method"], s["path"].format(scd_id=self.env.scd_id))
        data = res.json()
        check.equal(int(data["status"]), int(s["expected_res"]))
        self.handler.write_sheet('卸船', s['case_id'] + 1, 8, data["status"])

    def confirm_report(self):
        s = self.sheet[4]
        payload = json.loads(s["payload"])
        payload["scdId"] = [self.env.scd_id]
        res = self.request_main(s["method"], s["path"], json=payload)
        data = res.json()
        check.equal(int(data["status"]), int(s["expected_res"]))
        self.handler.write_sheet('卸船', s['case_id'] + 1, 8, data["status"])

    def confirm_report_cancel(self):
        s = self.sheet[5]
        payload = json.loads(s["payload"])
        payload["scdId"] = [self.env.scd_id]
        res = self.request_main(s["method"], s["path"], json=payload)
        data = res.json()
        check.equal(int(data["status"]), int(s["expected_res"]))
        self.handler.write_sheet('卸船', s['case_id'] + 1, 8, data["status"])

    def subarea(self):
        s = self.sheet[6]
        payload = json.loads(s["payload"])
        payload["scdId"] = [self.env.scd_id]
        res = self.request_main(s["method"], s["path"], json=payload)
        data = res.json()
        check.equal(int(data["status"]), int(s["expected_res"]))
        self.handler.write_sheet('卸船', s['case_id'] + 1, 8, data["status"])

    def subarea_cancel(self):
        s = self.sheet[7]
        payload = json.loads(s["payload"])
        payload["scdId"] = [self.env.scd_id]
        res = self.request_main(s["method"], s["path"], json=payload)
        data = res.json()
        check.equal(int(data["status"]), int(s["expected_res"]))
        self.handler.write_sheet('卸船', s['case_id'] + 1, 8, data["status"])

    def add_berth_plan(self):
        s = self.sheet[8]
        self.env.vbt_pbthdt = self.cus.get_datetime_now
        self.env.vbt_pdptdt = self.cus.get_datetime_add(self.env.vbt_pbthdt, day=1)
        payload = json.loads(s["payload"])
        payload["vbtScdId"] = self.env.scd_id
        payload["vbtPbthdt"] = self.env.vbt_pbthdt
        payload["vbtPdptdt"] = self.env.vbt_pdptdt
        res = self.request_main(s["method"], s["path"], json=payload)
        data = res.json()
        check.equal(int(data["status"]), int(s["expected_res"]))
        self.handler.write_sheet('卸船', s['case_id'] + 1, 8, data["status"])

    def add_ship_plan(self):
        s = self.sheet[9]
        self.env.dvp_opsttm = self.cus.get_datetime_add(self.env.vbt_pbthdt, minute=30)
        self.env.dvp_opedtm = self.cus.get_datetime_add(self.env.dvp_opsttm, day=1)
        self.env.dvp_opdate = self.cus.to_date(self.cus.get_datetime_add(self.env.vbt_pbthdt, day=-1))
        payload = json.loads(s["payload"])
        payload["dvpScdId"] = self.env.scd_id
        payload["dvpOpsttm"] = self.env.dvp_opsttm
        payload["dvpOpedtm"] = self.env.dvp_opedtm
        payload["dvpTrade"] = self.env.trade_type
        payload["dvpCargo"] = self.env.gtypecd
        payload["dvpVoyId"] = self.env.voy_id
        payload["dvpVoyage"] = self.env.voyage
        payload["dvpWgtTotal"] = self.env.gtwg
        payload["dvpIefg"] = self.env.iefg
        payload["dtsVesselRouteEntityList"][1]["dvrThroughput"] = self.env.gtwg
        payload["dtsVesselRouteEntityList"][1]["dvrOpproc"] = self.env.opproc_dc
        payload["dvpOpdate"] = self.env.dvp_opdate
        res = self.request_main(s["method"], s["path"], json=payload)
        data = res.json()
        if check.equal(int(data["status"]), int(s["expected_res"])):
            self.handler.write_sheet('卸船', s['case_id'] + 1, 8, data["status"])
            self.env.dvp_id = data["data"]["dvpId"]
            self.env.dc_route_id = data["data"]["dtsVesselRouteEntityList"][1]["dtsRouteMachinesEntityList"][0][
                "drmRouteId"]
        else:
            self.logger.error("新增大船作业计划失败")

    def delete_ship_plan(self):
        s = self.sheet[10]
        res = self.request_main(s["method"], s["path"].format(dvp_id=self.env.dvp_id))
        data = res.json()
        check.equal(int(data["status"]), int(s["expected_res"]))
        self.handler.write_sheet('卸船', s['case_id'] + 1, 8, data["status"])

    def add_bill(self):
        s = self.sheet[11]
        self.env.bill_no = self.cus.get_bill
        self.env.mark_no = self.cus.get_mark
        self.env.bill_type = "G"
        self.env.gname = self.db.select_from_table("select pck_kind_name "
                                                   "from pub_cargo_kind "
                                                   "where pck_kind_code='{gtypecd}'"
                                                   .format(gtypecd=self.env.gtypecd)).loc[0, 'pck_kind_name']
        payload = json.loads(s["payload"])
        payload["bilBillNbr"] = self.env.bill_no
        payload["bilBillTrade"] = self.env.trade_type
        payload["bilBillIefg"] = self.env.iefg
        payload["bilBillType"] = self.env.bill_type
        payload["busGoodsEntities"][0]["gdsMarkno"] = self.env.mark_no
        payload["busGoodsEntities"][0]["gdsGname"] = self.env.gname
        payload["busGoodsEntities"][0]["gdsGtpks"] = self.env.gtpks
        payload["busGoodsEntities"][0]["gdsGtwg"] = self.env.gtwg
        payload["busGoodsEntities"][0]["bpgPkgCode"] = [self.env.pktype]
        payload["busGoodsEntities"][0]["gdsGtvol"] = self.env.gtvol
        payload["busGoodsEntities"][0]["gdsGtypecd"] = self.env.gtypecd
        payload["busGoodsEntities"][0]["goodsPackagesEntityList"][0]["bpgPkgCode"] = self.env.pktype
        payload["bilVoyId"] = self.env.voy_id
        res = self.request_main(s["method"], s["path"], json=payload)
        data = res.json()
        if check.equal(int(data["status"]), int(s["expected_res"])):
            self.env.bil_id = data["data"]["bilId"]
        else:
            self.logger.error("新增舱单失败")

    def delete_bill(self):
        s = self.sheet[12]
        res = self.request_main(s["method"], s["path"].format(bil_id=self.env.bil_id))
        data = res.json()
        check.equal(int(data["status"]), int(s["expected_res"]))
        self.handler.write_sheet('卸船', s['case_id'] + 1, 8, data["status"])

    def add_shift_task(self, task_type):
        s = self.sheet[13]
        self.env.dst_type_dc = 'V'
        self.env.optype_dc = 'DC'
        self.env.dst_opdate = self.cus.get_datetime_add(self.env.dvp_opdate, day=1)
        payload = json.loads(s["payload"])
        payload["dtsShiftTaskEntities"][0]["dstRouteId"] = self.env.dc_route_id
        payload["dtsShiftTaskEntities"][0]["dstTaskType"] = self.env.dst_type_dc
        payload["dtsShiftTaskEntities"][0]["dstOpdate"] = self.env.dst_opdate
        payload["dtsShiftTaskEntities"][0]["dstShiftCode"] = self.env.shift
        payload["dtsShiftTaskEntities"][0]["dstOpproc"] = self.env.opproc_dc
        payload["dtsShiftTaskEntities"][0]["dstOptype"] = self.env.optype_dc
        payload["dtsShiftTaskEntities"][0]["dstPWgt"] = self.env.gtwg
        payload["dtsShiftTaskEntities"][0]["dstCargo"] = self.env.gtypecd
        payload["dtsShiftTaskEntities"][0]["dstPktype"] = self.env.pktype
        res = self.request_main(s["method"], s["path"], json=payload)
        data = res.json()
        if check.equal(int(data["status"]), int(s["expected_res"])):
            self.env.dc_dst_id = data["data"][0]["dstId"]
            self.env.dc_stm_id = data["data"][0]["shiftTaskMactypeEntities"][0]["stmId"]
            self.env.dc_stw_id = data["data"][0]["shiftTaskWkgroupEntities"][0]["stwId"]
        else:
            self.logger.error("新增当班任务失败")

    def delete_shift_task(self, task_type):
        s = self.sheet[14]
        dst_id = self.env.dc_dst_id if task_type == 'dc' else self.env.pk_dst_id
        res = self.request_main(s["method"], s["path"].format(dst_id=dst_id))
        data = res.json()
        check.equal(int(data["status"]), int(s["expected_res"]))

    def tally_attend(self):
        s = self.sheet[15]
        payload = json.loads(s["payload"])
        payload["dtsAttdWorkerEntities"][0]["dawDate"] = self.env.dst_opdate
        payload["dtsAttdWorkerEntities"][0]["dawShift"] = self.env.shift
        payload["dtsAttdWorkerEntities"][0]["dawEmpNo"] = self.env.emp_no
        payload["dtsAttdWorkerEntities"][0]["dawUserName"] = self.env.user_cnname
        payload["dtsAttdWorkerEntities"][0]["dawUserId"] = self.env.user_id
        payload["dtsAttdWorkerEntities"][0]["dawDeptName"] = self.env.user_dept_name
        payload["dtsAttdWorkerEntities"][0]["dawDeptId"] = self.env.user_dept_id
        res = self.request_main(s["method"], s["path"], json=payload)
        data = res.json()
        check.equal(int(data["status"]), int(s["expected_res"]))

    def tally_attend_cancel(self):
        s = self.sheet[41]
        payload = json.loads(s["payload"])
        # 理货员出勤id
        self.env.daw_id = \
            self.db.select_from_table("select daw_id "
                                      "from dts_attd_worker "
                                      "where daw_date = '{date}' and daw_shift = '{shift}' and daw_user_id = '{id}'"
                                      .format(date=self.env.dst_opdate, shift=self.env.shift, id=self.env.user_id)).loc[0, 'daw_id']
        payload["dawIds"] = [self.env.daw_id]
        res = self.request_main(s["method"], s["path"], json=payload)
        data = res.json()
        check.equal(int(data["status"]), int(s["expected_res"]))

    def tally_arrange(self):
        s = self.sheet[16]
        payload = json.loads(s["payload"])
        payload["dtsShiftTaskTallyEntityList"][0]["sttDstId"] = self.env.dc_dst_id
        payload["dtsShiftTaskTallyEntityList"][0]["sttUserId"] = self.env.user_id
        payload["dtsShiftTaskTallyEntityList"][0]["sttUserNm"] = self.env.user_cnname
        payload["dtsShiftTaskTallyEntityList"][0]["sttNunber"] = self.env.emp_no
        res = self.request_main(s["method"], s["path"], json=payload)
        data = res.json()
        if check.equal(int(data["status"]), int(s["expected_res"])):
            self.env.dc_stt_id = data["data"]["dtsShiftTaskTallyEntityList"][0]["sttId"]
        else:
            self.logger.error("理货员安排失败")

    def tally_arrange_remove(self):
        s = self.sheet[17]
        payload = json.loads(s["payload"])
        payload["sttIds"] = [self.env.dc_stt_id]
        res = self.request_main(s["method"], s["path"], json=payload)
        data = res.json()
        check.equal(int(data["status"]), int(s["expected_res"]))

    def machine_attend(self):
        s = self.sheet[18]
        payload = json.loads(s["payload"])
        payload["dtsYardWorkingMachinesEntities"][0]["ymaOpdate"] = self.env.dst_opdate
        payload["dtsYardWorkingMachinesEntities"][0]["ymaShift"] = self.env.shift
        res = self.request_main(s["method"], s["path"], json=payload)
        data = res.json()
        check.equal(int(data["status"]), int(s["expected_res"]))

    def machine_attend_cancel(self):
        s = self.sheet[42]
        payload = json.loads(s["payload"])
        payload["dywmIds"] = [self.env.yma_id]
        res = self.request_main(s["method"], s["path"], json=payload)
        data = res.json()
        check.equal(int(data["status"]), int(s["expected_res"]))

    def driver_arrange(self):
        s = self.sheet[19]
        payload = json.loads(s["payload"])
        # 机械出勤id
        self.env.yma_id = \
            self.db.select_from_table("select yma_id "
                                      "from dts_yard_working_machines yma "
                                      "join pub_yard_machines ymc on yma.yma_ymc_id=ymc.ymc_id "
                                      "where yma_opdate='{optype}' and yma_shift='{shift}'"
                                      " and ymc.ymc_mchno='{machine_no}' "
                                      .format(optype=self.env.dst_opdate, shift=self.env.shift,
                                              machine_no='4001')).loc[0, 'yma_id']
        payload["dtsYardWorkingMachinesEntities"][0]["ymaId"] = self.env.yma_id
        payload["dtsYardWorkingMachinesEntities"][0]["ymaOpdate"] = self.env.dst_opdate
        payload["dtsYardWorkingMachinesEntities"][0]["ymaShift"] = self.env.shift
        res = self.request_main(s["method"], s["path"], json=payload)
        data = res.json()
        check.equal(int(data["status"]), int(s["expected_res"]))

    def driver_arrange_delete(self):
        s = self.sheet[43]
        payload = json.loads(s["payload"])
        # 司机出勤id
        self.env.ydr_id = \
            self.db.select_from_table("select ydr_id "
                                      "from dts_yard_working_driver "
                                      "where ydr_yma_id = '{yma_id}'"
                                      .format(yma_id=self.env.yma_id)).loc[0, 'ydr_id']
        payload["dywdIds"] = [self.env.ydr_id]
        res = self.request_main(s["method"], s["path"], json=payload)
        data = res.json()
        check.equal(int(data["status"]), int(s["expected_res"]))

    def machine_arrange(self):
        s = self.sheet[20]
        self.env.dmc_sttm = self.cus.get_datetime_add(self.env.dst_opdate, hour=6)
        self.env.dmc_edtm = self.cus.get_datetime_add(self.env.dst_opdate, hour=18)
        payload = json.loads(s["payload"])
        self.env.instructor_config = \
            self.db.select_from_table("select stc_id "
                                      "from dts_shift_task_config "
                                      "where stc_dts_id='{dst_id}' and stc_type='2'"
                                      .format(dst_id=self.env.dc_dst_id)).loc[0, 'stc_id']
        payload["configId"] = self.env.instructor_config
        payload["machines"][0]["dmcDstId"] = self.env.dc_dst_id
        payload["machines"][0]["dmcYmaId"] = self.env.yma_id
        payload["machines"][0]["dmcSttm"] = self.env.dmc_sttm
        payload["machines"][0]["dmcEdtm"] = self.env.dmc_edtm
        res = self.request_main(s["method"], s["path"].format(instructor_config=self.env.instructor_config),
                                json=payload)
        data = res.json()
        check.equal(int(data["status"]), int(s["expected_res"]))

    def machine_diver_match(self):
        s = self.sheet[21]
        payload = json.loads(s["payload"])
        payload["stcId"] = self.env.instructor_config
        res = self.request_main(s["method"], s["path"], params=payload)
        data = res.json()
        check.equal(int(data["status"]), int(s["expected_res"]))

    def machine_arrange_remove(self):
        s = self.sheet[22]
        self.env.cma_id = \
            self.db.select_from_table("select cma_id "
                                      "from dts_shift_task_config_machine "
                                      "where cma_stc_id = '{instructor_config}'"
                                      .format(instructor_config=self.env.instructor_config)).loc[0, 'cma_id']
        payload = [self.env.cma_id]
        res = self.request_main(s["method"], s["path"], json=payload)
        data = res.json()
        check.equal(int(data["status"]), int(s["expected_res"]))

    def machine_arrange_delete(self):
        s = self.sheet[23]
        # 机械安排id
        self.env.dmc_id = \
            self.db.select_from_table("select dmc_id "
                                      "from dts_shift_task_machines "
                                      "where dmc_dst_id = '{dst_id}'"
                                      .format(dst_id=self.env.dc_dst_id)).loc[0, 'dmc_id']
        payload = json.loads(s["payload"])
        payload["dmcIds"] = [self.env.dmc_id]
        payload["dmcDstId"] = self.env.dc_dst_id
        res = self.request_main(s["method"], s["path"], json=payload)
        data = res.json()
        check.equal(int(data["status"]), int(s["expected_res"]))

    def workgroup_arrange(self):
        s = self.sheet[24]
        payload = json.loads(s["payload"])
        payload["dtsShiftTaskWkgroupList"][0]["createTime"] = self.cus.get_datetime_now
        payload["dtsShiftTaskWkgroupList"][0]["stwId"] = self.env.dc_stw_id
        payload["dtsShiftTaskWkgroupList"][0]["stwDstId"] = self.env.dc_dst_id
        payload["dtsShiftTaskWkgroupList"][0]["dtsShiftTaskConfigMacusrEntity"]["tcmStcId"] = self.env.instructor_config
        res = self.request_main(s["method"], s["path"], json=payload)
        data = res.json()
        check.equal(int(data["status"]), int(s["expected_res"]))

    def workgroup_arrange_delete(self):
        s = self.sheet[25]
        payload = json.loads(s["payload"])
        payload["stwIds"] = [self.env.dc_stw_id]
        payload["tcmStcIds"] = [self.env.instructor_config]
        res = self.request_main(s["method"], s["path"], json=payload)
        data = res.json()
        check.equal(int(data["status"]), int(s["expected_res"]))

    def berth(self):
        s = self.sheet[26]
        self.env.vbt_id = \
            self.db.select_from_table("select vbt_id "
                                      "from bps_vessel_berthes "
                                      "where vbt_scd_id = '{scd_id}'"
                                      .format(scd_id=self.env.scd_id)).loc[0, 'vbt_id']
        payload = json.loads(s["payload"])
        payload["vbtScdId"] = self.env.scd_id
        payload["vbtAbthdt"] = self.cus.get_datetime_now
        payload["vbtId"] = self.env.vbt_id
        payload["scdRStartTime"] = self.env.dvp_opsttm
        payload["scdREndTime"] = self.env.dvp_opedtm
        res = self.request_main(s["method"], s["path"], json=payload)
        data = res.json()
        check.equal(int(data["status"]), int(s["expected_res"]))

    def dc_tally_report(self):
        s = self.sheet[27]
        self.env.dc_barcode = \
            self.db.select_from_table("select gds_bar_code "
                                      "from bus_goods "
                                      "where gds_bil_id = '{bil_id}' "
                                      .format(bil_id=self.env.bil_id)).loc[0, 'gds_bar_code']
        self.env.location = \
            self.db.select_from_table("select ygc_id "
                                      "from pub_yard_goods_location "
                                      "where ygc_no = '{ygc_no}' "
                                      .format(ygc_no=self.env.ygc_no)).loc[0, 'ygc_id']
        payload = json.loads(s["payload"])
        payload["barCode"] = self.env.dc_barcode
        payload["billNo"] = self.env.bill_no
        payload["markNo"] = self.env.mark_no
        payload["cargoKind"] = self.env.gtypecd
        payload["zdConfig"] = self.env.instructor_config
        payload["taskId"] = self.env.dc_dst_id
        payload["shift"] = self.env.shift
        payload["location"] = self.env.location
        payload["pieces"] = self.env.gtpks
        payload["pkgType"] = self.env.pktype
        payload["opproc"] = self.env.opproc_dc
        payload["ptNum"] = float(self.env.gtwg) / float(self.env.gtpks)
        payload["weight"] = self.env.gtwg
        payload["volumn"] = self.env.gtvol
        payload["voyId"] = self.env.voy_id
        payload["empId"] = self.env.user_id
        res = self.request_main(s["method"], s["path"], json=payload)
        data = res.json()
        if check.equal(int(data["status"]), int(s["expected_res"])):
            self.env.dc_goa_id = \
                self.db.select_from_table("select goa_id "
                                          "from wms_goods_occupy_activities "
                                          "where goa_dst_id = '{dst_id}'"
                                          .format(dst_id=self.env.dc_dst_id)).loc[0, 'goa_id']
        else:
            self.logger.error("新增卸船汇报失败")

    def tally_report_delete(self, task_type):
        s = self.sheet[28]
        goa_id = self.env.dc_goa_id if task_type == 'dc' else self.env.pk_goa_id
        payload = [goa_id]
        res = self.request_main(s["method"], s["path"], json=payload)
        data = res.json()
        check.equal(int(data["status"]), int(s["expected_res"]))

    def tally_report_audit(self, task_type):
        s = self.sheet[29]
        goa_id = self.env.dc_goa_id if task_type == 'dc' else self.env.pk_goa_id
        payload = json.loads(s["payload"])
        res = self.request_main(s["method"], s["path"].format(goa_id=goa_id), params=payload)
        data = res.json()
        check.equal(int(data["status"]), int(s["expected_res"]))

    def tally_report_audit_cancel(self, task_type):
        s = self.sheet[30]
        goa_id = self.env.dc_goa_id if task_type == 'dc' else self.env.pk_goa_id
        payload = json.loads(s["payload"])
        res = self.request_main(s["method"], s["path"].format(goa_id=goa_id), params=payload)
        data = res.json()
        check.equal(int(data["status"]), int(s["expected_res"]))

    def task_audit(self, task_type):
        s = self.sheet[31]
        dst_id = self.env.dc_dst_id if task_type == 'dc' else self.env.pk_dst_id
        payload = json.loads(s["payload"])
        payload["staDstId"] = dst_id
        res = self.request_main(s["method"], s["path"], json=payload)
        data = res.json()
        check.equal(int(data["status"]), int(s["expected_res"]))

    def task_audit_cancel(self, task_type):
        s = self.sheet[32]
        dst_id = self.env.dc_dst_id if task_type == 'dc' else self.env.pk_dst_id
        payload = json.loads(s["payload"])
        payload["dstId"] = dst_id
        res = self.request_main(s["method"], s["path"], params=payload)
        data = res.json()
        check.equal(int(data["status"]), int(s["expected_res"]))

    def worksheet_wk_generate(self, task_type):
        s = self.sheet[33]
        dst_id = self.env.dc_dst_id if task_type == 'dc' else self.env.pk_dst_id
        if task_type == 'dc':
            self.env.dc_pws_id = \
                self.db.select_from_table("select pws_id "
                                          "from pws_work_sheet "
                                          "where pws_dts_id = '{dst_id}'"
                                          .format(dst_id=dst_id)).loc[0, 'pws_id']
        else:
            self.env.pk_pws_id = \
                self.db.select_from_table("select pws_id "
                                          "from pws_work_sheet "
                                          "where pws_dts_id = '{dst_id}'"
                                          .format(dst_id=dst_id)).loc[0, 'pws_id']
        pws_id = self.env.dc_pws_id if task_type == 'dc' else self.env.pk_pws_id
        res = self.request_main(s["method"], s["path"].format(pws_id=pws_id))
        data = res.json()
        check.equal(int(data["status"]), int(s["expected_res"]))

    def worksheet_machine_generate(self, task_type):
        s = self.sheet[34]
        pws_id = self.env.dc_dst_id if task_type == 'dc' else self.env.pk_dst_id
        res = self.request_main(s["method"], s["path"].format(pws_id=self.env.dc_pws_id))
        data = res.json()
        check.equal(int(data["status"]), int(s["expected_res"]))

    def worksheet_wk_delete(self, task_type):
        s = self.sheet[35]
        pws_id = self.env.dc_pws_id if task_type == 'dc' else self.env.pk_pws_id
        self.env.dc_wsw_id = \
            self.db.select_from_table("select wsw_id "
                                      "from pws_work_sheet_wk "
                                      "where wsw_pws_id = '{pws_id}'"
                                      .format(pws_id=pws_id)).loc[0, 'wsw_id']
        res = self.request_main(s["method"], s["path"].format(wsw_id=self.env.dc_wsw_id))
        data = res.json()
        check.equal(int(data["status"]), int(s["expected_res"]))

    def worksheet_control_audit(self, task_type):
        s = self.sheet[36]
        pws_id = self.env.dc_pws_id if task_type == 'dc' else self.env.pk_pws_id
        payload = json.loads(s["payload"])
        payload["pwsId"] = pws_id
        res = self.request_main(s["method"], s["path"], json=payload)
        data = res.json()
        check.equal(int(data["status"]), int(s["expected_res"]))

    def worksheet_control_audit_cancel(self, task_type):
        s = self.sheet[37]
        pws_id = self.env.dc_pws_id if task_type == 'dc' else self.env.pk_pws_id
        payload = json.loads(s["payload"])
        payload["pwsId"] = pws_id
        res = self.request_main(s["method"], s["path"], json=payload)
        data = res.json()
        check.equal(int(data["status"]), int(s["expected_res"]))

    def worksheet_hr_audit(self, task_type):
        s = self.sheet[38]
        pws_id = self.env.dc_pws_id if task_type == 'dc' else self.env.pk_pws_id
        payload = json.loads(s["payload"])
        payload["pwsId"] = pws_id
        res = self.request_main(s["method"], s["path"], json=payload)
        data = res.json()
        check.equal(int(data["status"]), int(s["expected_res"]))

    def worksheet_hr_audit_cancel(self, task_type):
        s = self.sheet[39]
        pws_id = self.env.dc_pws_id if task_type == 'dc' else self.env.pk_pws_id
        payload = json.loads(s["payload"])
        payload["pwsId"] = pws_id
        res = self.request_main(s["method"], s["path"], json=payload)
        data = res.json()
        check.equal(int(data["status"]), int(s["expected_res"]))

    def get_user(self):
        s = self.sheet[40]
        payload = json.loads(s["payload"])
        payload["name"] = "罗泾管理员"
        res = self.request_main(s["method"], s["path"], params=payload)
        data = res.json()
        if check.equal(int(data["status"]), int(s["expected_res"])):
            self.handler.write_sheet('卸船', s['case_id'] + 1, 8, data["status"])
            self.env.user_id = data["data"]["records"][0]["id"]
            self.env.user_enname = data["data"]["records"][0]["account"]
            self.env.user_cnname = data["data"]["records"][0]["name"]
            self.env.emp_no = data["data"]["records"][0]["empNumber"]
            self.env.user_dept_id = data["data"]["records"][0]["depts"][0]["deptId"]
            self.env.user_dept_name = data["data"]["records"][0]["depts"][0]["deptName"]
        else:
            self.logger.error("获取用户信息失败")
