# -*- coding:utf-8 -*-
import os
import allure
import pytest
from pytest_check import check
from BTOSLJ.PageObject.request_lj.unship_n import UnshipN


@allure.epic('罗泾进口业务')
@allure.feature('内贸')
@allure.story('卸船提货')
@allure.title('船期维护')
def test_01_schedule(host):
    obj = UnshipN(host)
    obj.test_get_user()
    obj.set_values()
    with allure.step("大船维护"):
        obj.test_add_vessel()
    with allure.step("新增船期"):
        obj.test_add_schedule()
    with allure.step("确报"):
        obj.test_confirm_report()
    with allure.step("分区"):
        obj.test_subarea()


@allure.epic('罗泾进口业务')
@allure.feature('内贸')
@allure.story('卸船提货')
@allure.title('靠泊计划')
def test_02_berth_plan(host):
    obj = UnshipN(host)
    with allure.step("新增靠泊计划"):
        obj.test_add_berth_plan()


@allure.epic('罗泾进口业务')
@allure.feature('内贸')
@allure.story('卸船提货')
@allure.title('新增内贸进口舱单')
def test_03_bill(host):
    obj = UnshipN(host)
    with allure.step("新增内贸进口舱单"):
        obj.test_add_bill()


@allure.epic('罗泾进口业务')
@allure.feature('内贸')
@allure.story('卸船提货')
@allure.title('新增大船作业计划')
def test_04_ship_plan(host):
    obj = UnshipN(host)
    with allure.step("新增大船作业计划"):
        obj.test_add_ship_plan()


@allure.epic('罗泾进口业务')
@allure.feature('内贸')
@allure.story('卸船提货')
@allure.title('新增卸船任务')
def test_05_task_dc(host):
    obj = UnshipN(host)
    with allure.step("新增当班任务"):
        obj.test_add_shift_task('dc')


@allure.epic('罗泾进口业务')
@allure.feature('内贸')
@allure.story('卸船提货')
@allure.title('理货员出勤')
def test_06_tally_attend(host):
    obj = UnshipN(host)
    with allure.step("理货员出勤"):
        obj.test_tally_attend()


@allure.epic('罗泾进口业务')
@allure.feature('内贸')
@allure.story('卸船提货')
@allure.title('机械出勤')
def test_07_machine_attend(host):
    obj = UnshipN(host)
    with allure.step("机械出勤"):
        obj.test_machine_attend()
        obj.test_driver_arrange()


@allure.epic('罗泾进口业务')
@allure.feature('内贸')
@allure.story('卸船提货')
@allure.title('卸船任务管理')
def test_08_task_manage_dc(host):
    obj = UnshipN(host)
    with allure.step("理货员安排"):
        obj.test_tally_arrange()
    with allure.step("机械人员配置"):
        obj.test_machine_arrange()
    with allure.step("机械司机匹配"):
        obj.test_machine_diver_match()
    with allure.step("劳务队安排"):
        obj.test_workgroup_arrange()


@allure.epic('罗泾进口业务')
@allure.feature('内贸')
@allure.story('卸船提货')
@allure.title('实际靠泊')
def test_09_berth(host):
    obj = UnshipN(host)
    with allure.step("实际靠泊"):
        obj.test_berth()


@allure.epic('罗泾进口业务')
@allure.feature('内贸')
@allure.story('卸船提货')
@allure.title('卸船汇报')
def test_10_tally_report_dc(host):
    obj = UnshipN(host)
    with allure.step("理货汇报"):
        obj.test_dc_tally_report()
    with allure.step("理货动态审核"):
        obj.test_tally_report_audit('dc')
    with allure.step("工班任务审核"):
        obj.test_task_audit('dc')


@allure.epic('罗泾进口业务')
@allure.feature('内贸')
@allure.story('卸船提货')
@allure.title('作业票')
def test_11_worksheet_dc(host):
    obj = UnshipN(host)
    with allure.step("生成装卸队作业票"):
        obj.test_worksheet_wk_generate('dc')
    with allure.step("生成员工作业票"):
        obj.test_worksheet_machine_generate('dc')
    with allure.step("中控审核"):
        obj.test_worksheet_control_audit('dc')
    with allure.step("人事审核"):
        obj.test_worksheet_hr_audit('dc')


@allure.epic('罗泾进口业务')
@allure.feature('内贸')
@allure.story('卸船提货')
@allure.title('回退')
def test_12_rollback(host):
    obj = UnshipN(host)
    with allure.step("取消人事审核"):
        obj.test_worksheet_hr_audit_cancel('dc')
    with allure.step("取消中控审核"):
        obj.test_worksheet_control_audit_cancel('dc')
    with allure.step("删除作业票"):
        obj.test_worksheet_wk_delete('dc')
    with allure.step("取消工班任务审核"):
        obj.test_task_audit_cancel('dc')
    with allure.step("取消卸船汇报审核"):
        obj.test_tally_report_audit_cancel('dc')
    with allure.step("删除卸船汇报"):
        obj.test_tally_report_delete("dc")
    with allure.step("删除劳务队配置"):
        obj.test_workgroup_arrange_delete()
    with allure.step("删除机械人员配置"):
        obj.test_machine_arrange_remove()
    with allure.step("取消机械安排"):
        obj.test_machine_arrange_delete()
    with allure.step("取消理货员安排"):
        obj.test_tally_arrange_remove()
    with allure.step("删除工班任务"):
        obj.test_delete_shift_task("dc")
    with allure.step("删除大船作业计划"):
        obj.test_delete_ship_plan()
    with allure.step("删除内贸进口舱单"):
        obj.test_delete_bill()
    with allure.step("删除船期"):
        obj.test_delete_schedule()
    with allure.step("删除大船"):
        obj.test_delete_vessel()





