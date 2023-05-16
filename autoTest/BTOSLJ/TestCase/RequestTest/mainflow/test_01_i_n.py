# -*- coding:utf-8 -*-
import allure
import pytest
from BTOSLJ.PageObject.request_lj.unship_n import UnshipN
from BTOSLJ.PageObject.request_lj.pickup_n import PickupN
from config import host, header


@allure.epic('罗泾进口业务')
@allure.feature('内贸')
@allure.story('卸船提货')
class TestUnshipPickupN:
    def setup_class(self):
        h1 = host()
        h2 = header()
        self.obj = UnshipN(h1, h2)
        self.pbj = PickupN(h1, h2)
        self.obj.get_user()
        self.obj.set_values()

    @allure.title('船舶维护')
    @pytest.mark.skip
    def test_01_vessel(self):
        with allure.step("大船维护"):
            self.obj.add_vessel()

    @allure.title('船期维护')
    def test_02_schedule(self):
        self.obj.logger.info("内贸进口流程-卸船")
        with allure.step("新增船期"):
            self.obj.add_schedule()
        with allure.step("确报"):
            self.obj.confirm_report()
        with allure.step("分区"):
            self.obj.subarea()

    @allure.title('靠泊计划')
    def test_03_berth_plan(self):
        with allure.step("新增靠泊计划"):
            self.obj.add_berth_plan()

    @allure.title('内贸进口舱单')
    def test_04_bill(self):
        with allure.step("新增内贸进口舱单"):
            self.obj.add_bill()

    @allure.title('大船作业计划')
    def test_05_ship_plan(self):
        with allure.step("新增大船作业计划"):
            self.obj.add_ship_plan()

    @allure.title('卸船任务')
    def test_06_task_dc(self):
        with allure.step("新增当班任务"):
            self.obj.add_shift_task_dc()

    @allure.title('理货员出勤')
    def test_07_tally_attend(self):
        with allure.step("理货员出勤"):
            self.obj.tally_attend()

    @allure.title('机械出勤')
    def test_08_machine_attend(self):
        with allure.step("机械出勤"):
            self.obj.machine_attend()
            self.obj.driver_arrange()

    @allure.title('卸船任务管理')
    def test_09_task_manage_dc(self):
        with allure.step("理货员安排"):
            self.obj.tally_arrange('dc')
        with allure.step("机械人员配置"):
            self.obj.machine_arrange()
        with allure.step("机械司机匹配"):
            self.obj.machine_diver_match()
        with allure.step("劳务队安排"):
            self.obj.workgroup_arrange('dc')

    @allure.title('实际靠泊')
    def test_10_berth(self):
        with allure.step("实际靠泊"):
            self.obj.berth()

    @allure.title('卸船汇报')
    def test_11_tally_report_dc(self):
        with allure.step("理货汇报"):
            self.obj.dc_tally_report()
        with allure.step("理货动态审核"):
            self.obj.tally_report_audit('dc')
        with allure.step("工班任务审核"):
            self.obj.dc_task_audit()

    @allure.title('卸船作业票')
    def test_12_worksheet_dc(self):
        with allure.step("生成作业票"):
            self.obj.generate_worksheet('dc')
        with allure.step("生成装卸队作业票"):
            self.obj.worksheet_wk_generate('dc')
        with allure.step("生成员工作业票"):
            self.obj.worksheet_machine_generate('dc')
        with allure.step("中控审核"):
            self.obj.worksheet_control_audit('dc')
        with allure.step("人事审核"):
            self.obj.worksheet_hr_audit('dc')

    @allure.title('提货受理')
    def test_13_accept(self):
        self.obj.logger.info("内贸进口流程-提货")
        with allure.step("新增提货受理"):
            self.pbj.add_accept()

    @allure.title('车驳作业计划')
    def test_14_warehouse_plan(self):
        with allure.step("新增车驳作业计划"):
            self.pbj.add_warehouse_plan()

    @allure.title('提货任务')
    def test_15_task_pk(self):
        with allure.step("新增提货当班任务"):
            self.pbj.add_shift_task_pk()

    @allure.title('提货任务管理')
    def test_16_task_pk_manage(self):
        with allure.step("理货员安排"):
            self.obj.tally_arrange('pk')
        with allure.step("库场安排"):
            self.pbj.warehouse_arrange()
        with allure.step("作业票汇报配置"):
            self.obj.workgroup_arrange('pk')

    @allure.title('提货汇报')
    def test_17_tally_report_pk(self):
        with allure.step("新增提货汇报"):
            self.pbj.pk_tally_report()
        with allure.step("理货动态审核"):
            self.obj.tally_report_audit('pk')
        with allure.step("工班任务审核"):
            self.pbj.pk_task_audit()
        with allure.step("新增进门记录"):
            self.pbj.outdoor_pass()

    @allure.title('提货作业票')
    def test_18_worksheet_pk(self):
        with allure.step("生成作业票"):
            self.obj.generate_worksheet('pk')
        with allure.step("生成装卸队作业票"):
            self.obj.worksheet_wk_generate('pk')
        with allure.step("生成员工作业票"):
            self.obj.worksheet_machine_generate('pk')
        with allure.step("中控审核"):
            self.obj.worksheet_control_audit('pk')
        with allure.step("人事审核"):
            self.obj.worksheet_hr_audit('pk')

    @allure.title('离泊')
    def test_19_unberth(self):
        with allure.step("船舶离泊"):
            self.obj.unberth()

    @allure.title('提货回退')
    # @pytest.mark.skip
    def test_20_rollback_pk(self):
        with allure.step("取消人事审核"):
            self.obj.worksheet_hr_audit_cancel('pk')
        with allure.step("取消中控审核"):
            self.obj.worksheet_control_audit_cancel('pk')
        with allure.step("删除作业票"):
            self.obj.worksheet_delete('pk')
        with allure.step("取消工班任务审核"):
            self.obj.task_audit_cancel('pk')
        with allure.step("取消提货汇报审核"):
            self.obj.tally_report_audit_cancel('pk')
        with allure.step("删除提货汇报"):
            self.obj.tally_report_delete("pk")
        with allure.step("删除劳务队配置"):
            self.obj.workgroup_arrange_delete('pk')
        with allure.step("取消理货员安排"):
            self.obj.tally_arrange_remove('pk')
        with allure.step("取消库场安排"):
            self.pbj.warehouse_arrange_cancel()
        with allure.step("删除工班任务"):
            self.obj.delete_shift_task("pk")
        with allure.step("删除车驳作业计划"):
            self.pbj.delete_warehouse_plan()
        with allure.step("删除内贸提货受理"):
            self.pbj.delete_accept()

    @allure.title('卸船回退')
    # @pytest.mark.skip
    def test_21_rollback_dc(self):
        with allure.step("取消人事审核"):
            self.obj.worksheet_hr_audit_cancel('dc')
        with allure.step("取消中控审核"):
            self.obj.worksheet_control_audit_cancel('dc')
        with allure.step("删除作业票"):
            self.obj.worksheet_delete('dc')
        with allure.step("取消工班任务审核"):
            self.obj.task_audit_cancel('dc')
        with allure.step("取消卸船汇报审核"):
            self.obj.tally_report_audit_cancel('dc')
        with allure.step("删除卸船汇报"):
            self.obj.tally_report_delete("dc")
        with allure.step("删除劳务队配置"):
            self.obj.workgroup_arrange_delete('dc')
        with allure.step("删除机械人员配置"):
            self.obj.machine_arrange_remove()
        with allure.step("取消机械安排"):
            self.obj.machine_arrange_delete()
        with allure.step("取消理货员安排"):
            self.obj.tally_arrange_remove('dc')
        with allure.step("取消理货员出勤"):
            self.obj.tally_attend_cancel()
        with allure.step("取消司机出勤"):
            self.obj.driver_arrange_delete()
        with allure.step("取消机械出勤"):
            self.obj.machine_attend_cancel()
        with allure.step("删除工班任务"):
            self.obj.delete_shift_task("dc")
        with allure.step("删除大船作业计划"):
            self.obj.delete_ship_plan()
        with allure.step("删除内贸进口舱单"):
            self.obj.delete_bill()
        '''
        with allure.step("删除船期"):
            self.obj.delete_schedule()
        with allure.step("删除大船"):
            self.obj.delete_vessel()
            pass
        '''

    def teardown_class(self):
        del self.pbj
        del self.obj




