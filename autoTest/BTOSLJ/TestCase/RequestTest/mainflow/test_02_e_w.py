# -*- coding:utf-8 -*-
# Developer         : baishijun
# Development Time  : 2023/5/15 16:55
# Document Name     : test_02_e_w.PY
# Development Tool  : PyCharm


import allure
import pytest
from BTOSLJ.PageObject.request_lj.deliver_w import DeliverW
from BTOSLJ.PageObject.request_lj.ship_w import ShipW
from config import host, header


@allure.epic('罗泾出口业务')
@allure.feature('外贸')
@allure.story('进货装船')
class TestDeliverShipW:
    def setup_class(self):
        h1 = host()
        h2 = header()
        self.de = DeliverW(h1, h2)
        self.ld = ShipW(h1, h2)
        self.de.get_user()
        self.de.set_values()

    @allure.title('船舶维护')
    @pytest.mark.skip
    def test_01_vessel(self):
        with allure.step("大船维护"):
            self.de.add_vessel()

    @allure.title('船期维护')
    def test_02_schedule(self):
        self.de.logger.info("外贸出口流程-进货")
        with allure.step("新增船期"):
            self.de.add_schedule()
        with allure.step("确报"):
            self.de.confirm_report()
        with allure.step("分区"):
            self.de.subarea()

    @allure.title('靠泊计划')
    def test_03_berth_plan(self):
        with allure.step("新增靠泊计划"):
            self.de.add_berth_plan()

    @allure.title('进货受理')
    def test_04_accept(self):
        with allure.step("新增外贸进货受理"):
            self.de.add_accept_w()

    @allure.title('车驳作业计划')
    def test_05_warehouse_plan(self):
        with allure.step("新增外贸进货受理"):
            self.de.add_warehouse_plan()

    @allure.title('新增进货任务')
    def test_06_task_de(self):
        with allure.step("新增进货当班任务"):
            self.de.add_shift_task_de()

    @allure.title('理货员出勤')
    def test_07_tally_attend(self):
        with allure.step("理货员出勤"):
            self.de.tally_attend()

    @allure.title('进货任务管理')
    def test_08_task_manage_dc(self):
        with allure.step("理货员安排"):
            self.de.tally_arrange('de')
        with allure.step("劳务队安排"):
            self.de.workgroup_arrange('de')

    @allure.title('进栈预录')
    def test_09_prerecording(self):
        with allure.step("新增预录"):
            self.de.add_stack_prerecording()

    @allure.title('进门道口放行')
    def test_10_indoor_pass(self):
        with allure.step("道口校验"):
            self.de.in_door_check()
        with allure.step("进门放行"):
            self.de.in_door_pass()

    @allure.title('进货汇报')
    def test_11_tally_report_de(self):
        with allure.step("新增理货汇报"):
            self.de.tally_report_de('W')
        with allure.step("理货动态审核"):
            self.de.tally_report_audit('de')
        with allure.step("作业路审核"):
            self.de.de_task_audit()

    @allure.title('出门道口放行')
    def test_12_outdoor_pass(self):
        with allure.step("出门放行"):
            self.de.out_door_pass()

    @allure.title('进货作业票')
    def test_13_worksheet_de(self):
        with allure.step("生成装卸队作业票"):
            self.de.worksheet_wk_generate('de')
        with allure.step("生成员工作业票"):
            self.de.worksheet_machine_generate('de')
        with allure.step("中控审核"):
            self.de.worksheet_control_audit('de')
        with allure.step("人事审核"):
            self.de.worksheet_hr_audit('de')

    @allure.title('新增舱单')
    def test_14_add_bill(self):
        self.ld.logger.info("外贸出口流程-装船")
        with allure.step("新增外贸出口舱单"):
            self.ld.add_bill()

    @allure.title('配货')
    def test_15_allocat_goods(self):
        with allure.step("在场货关联舱单"):
            self.ld.allocat_goods()

    @allure.title('大船作业计划')
    def test_16_vessel_plan(self):
        with allure.step("新增大船作业计划"):
            self.ld.add_vessel_plan()

    @allure.title('新增装船任务')
    def test_17_add_task_ld(self):
        with allure.step("新增装船当班任务"):
            self.ld.add_shift_task_ld()

    @allure.title('机械出勤')
    def test_18_machine_attend(self):
        with allure.step("机械出勤"):
            self.ld.machine_attend()
        with allure.step("安排司机"):
            self.ld.driver_arrange()

    @allure.title('装船任务管理')
    def test_19_task_manage(self):
        with allure.step("机械人员配置"):
            self.ld.machine_arrange()
        with allure.step("机械匹配司机"):
            self.ld.machine_diver_match()
        with allure.step("库场安排"):
            self.ld.warehouse_arrange()
        with allure.step("劳务队安排"):
            self.de.workgroup_arrange('ld')

    @allure.title('实际靠泊')
    def test_20_berth(self):
        with allure.step("靠泊"):
            self.ld.berth()

    @allure.title('装船汇报')
    def test_21_tally_report_ld(self):
        with allure.step("新增理货汇报"):
            self.ld.tally_report_ld()
        with allure.step("理货动态审核"):
            self.de.tally_report_audit('ld')
        with allure.step("作业路审核"):
            self.ld.ld_task_audit()

    @allure.title('装船作业票')
    def test_22_worksheet_ld(self):
        with allure.step("生成装卸队作业票"):
            self.de.worksheet_wk_generate('ld')
        with allure.step("生成员工作业票"):
            self.de.worksheet_machine_generate('ld')
        with allure.step("中控审核"):
            self.de.worksheet_control_audit('ld')
        with allure.step("人事审核"):
            self.de.worksheet_hr_audit('ld')

    @allure.title('离泊')
    def test_23_unberth(self):
        with allure.step("船舶离泊"):
            self.ld.unberth()

    @allure.title('装船回退')
    # @pytest.mark.skip
    def test_24_rollback_ld(self):
        with allure.step("取消人事审核"):
            self.de.worksheet_hr_audit_cancel('ld')
        with allure.step("取消中控审核"):
            self.de.worksheet_control_audit_cancel('ld')
        with allure.step("删除作业票"):
            self.de.worksheet_delete('ld')
        with allure.step("取消作业路审核"):
            self.de.task_audit_cancel('ld')
        with allure.step("取消理货动态审核"):
            self.de.tally_report_audit_cancel('ld')
        with allure.step("删除理货动态"):
            self.de.delete_tally_report('ld')
        with allure.step("删除劳务队安排"):
            self.de.workgroup_arrange_delete('ld')
        with allure.step("删除理货员安排"):
            self.de.tally_arrange_remove('ld')
        with allure.step("删除机械安排"):
            self.ld.machine_arrange_remove()
            self.ld.machine_arrange_delete()
        with allure.step("取消机械出勤"):
            self.ld.driver_arrange_delete()
            self.ld.machine_attend_cancel()
        with allure.step("删除库场安排"):
            self.ld.warehouse_arrange_cancel()
        with allure.step("删除当班任务"):
            self.de.delete_shift_task('ld')
        with allure.step("删除大船作业计划"):
            self.ld.delete_vessel_plan()
        with allure.step("取消配货"):
            self.ld.allocat_goods_cancel()
        with allure.step("删除舱单"):
            self.ld.delete_bill()

    @allure.title('进货回退')
    # @pytest.mark.skip
    def test_25_rollback_de(self):
        with allure.step("取消人事审核"):
            self.de.worksheet_hr_audit_cancel('de')
        with allure.step("取消中控审核"):
            self.de.worksheet_control_audit_cancel('de')
        with allure.step("删除作业票"):
            self.de.worksheet_delete('de')
        with allure.step("取消作业路审核"):
            self.de.task_audit_cancel('de')
        with allure.step("取消理货动态审核"):
            self.de.tally_report_audit_cancel('de')
        with allure.step("删除理货动态"):
            self.de.delete_tally_report('de')
        with allure.step("删除劳务队安排"):
            self.de.workgroup_arrange_delete('de')
        with allure.step("删除理货员安排"):
            self.de.tally_arrange_remove('de')
        with allure.step("取消理货员出勤"):
            self.de.tally_attend_cancel()
        with allure.step("删除当班任务"):
            self.de.delete_shift_task('de')
        with allure.step("删除车驳作业计划"):
            self.de.delete_warehouse_plan()
        with allure.step("删除进货受理"):
            self.de.delete_accept()
        '''
        with allure.step("删除船期"):
            self.de.delete_schedule()
        '''

    def teardown_class(self):
        del self.de
        del self.ld

