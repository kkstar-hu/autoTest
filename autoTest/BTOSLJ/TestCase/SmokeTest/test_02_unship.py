import os
import time
import allure
import pytest
from BTOSLJ.Config import config
from BTOSLJ.PageObject.center_control.job_task import JobTask
from BTOSLJ.PageObject.center_control.mechanical_attendance import MechanicalAttendance
from BTOSLJ.PageObject.center_control.ship_stop_leave import Ship_Leave_Stop
from BTOSLJ.PageObject.center_control.work_task import WorkTask
from BTOSLJ.PageObject.center_control.work_task_report import WorkTaskReport
from BTOSLJ.PageObject.piece_wage.job_slip_center_control import JobSlipControl
from BTOSLJ.PageObject.piece_wage.job_slip_center_personnel import JobSlipPersonnel
from BTOSLJ.PageObject.plan_management.bigship_workplan import BigShipWorkPlan
from BTOSLJ.PageObject.store_management.Import_store_bill_management import ImStoreBill
from BTOSLJ.PageObject.store_management.tallyman_manage import Tallyman
from Commons.menu import Menu
from Commons.yamlread import read_yaml


@allure.story('一、卸船流程')
@allure.title('1.新增仓单')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(), 'unship.yaml')))
def test_add_store_bill(driver, input):
    menu = Menu(driver)
    menu.select_level_Menu("仓库管理,内贸进口仓库管理,内贸进口舱单管理")
    ship_bill = ImStoreBill(driver)
    ship_bill.add_bill(config.importNumber, input)
    ship_bill.check_table_bill(input)
    ship_bill.check_table_goods(input)


@allure.story('一、卸船流程')
@allure.title('2.安排大船作业计划')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(), 'unship.yaml')))
def test_add_work_plan(driver, input):
    menu = Menu(driver)
    menu.select_level_Menu("计划管理,大船作业计划")
    ship_work_plan = BigShipWorkPlan(driver)
    ship_work_plan.add_plan(config.importNumber, input)
    ship_work_plan.check_table_plan(input)


@allure.story('一、卸船流程')
@allure.title('3.当班作业任务')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(), 'unship.yaml')))
def test_add_work_task(driver, input):
    menu = Menu(driver)
    menu.select_level_Menu("中控调度,当班作业任务")
    work_task = WorkTask(driver)
    work_task.search(input)
    work_task.add_plan(input)
    time.sleep(0.5)
    work_task.check_table_task(input)


@allure.story('一、卸船流程')
@allure.title('5.理货员出勤')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(), 'unship.yaml')))
def test_tallyman_work(driver, input):
    menu = Menu(driver)
    menu.select_level_Menu("仓库管理,理货员出勤")
    tallyman = Tallyman(driver)
    tallyman.select_people(input)


@allure.story('一、卸船流程')
@allure.title('5.理货员安排')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(), 'unship.yaml')))
def test_tallyman_arrange(driver, input):
    menu = Menu(driver)
    menu.select_level_Menu("中控调度,作业任务管理")
    tallyman = JobTask(driver)
    tallyman.search(input)
    tallyman.check_table_task(input)
    tallyman.arrange_tallyman(input)


@allure.story('一、卸船流程')
@allure.title('6.机械出勤')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(), 'unship.yaml')))
def test_mechanical_attend(driver, input):
    menu = Menu(driver)
    menu.select_level_Menu("中控调度,机械出勤")
    mechanical = MechanicalAttendance(driver)
    mechanical.search(input)
    mechanical.arrange_mechanical(input)
    mechanical.arrange_driver(input)
    mechanical.check_table(input)


@allure.story('一、卸船流程')
@allure.title('7.机械安排')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(), 'unship.yaml')))
def test_mechanical_arrange(driver, input):
    menu = Menu(driver)
    menu.select_level_Menu("中控调度,作业任务管理")
    mechanical = JobTask(driver)
    mechanical.search(input)
    mechanical.arrange_machine(input)


@allure.story('一、卸船流程')
@allure.title('9.作业票汇报配置')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(), 'unship.yaml')))
def test_report_config(driver, input):
    menu = Menu(driver)
    menu.select_level_Menu("中控调度,作业任务管理")
    report_config = JobTask(driver)
    report_config.search(input)
    report_config.report_config(input)


@allure.story('一、卸船流程')
@allure.title('10.大船靠泊')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(), 'unship.yaml')))
def test_ship_leave_stop(driver, input):
    menu = Menu(driver)
    menu.select_level_Menu("中控调度,大船靠离泊管理")
    stop = Ship_Leave_Stop(driver)
    stop.search()
    stop.berthing_by()


@allure.story('一、卸船流程')
@allure.title('11.作业任务汇报')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(), 'unship.yaml')))
def test_task_report(driver, input):
    menu = Menu(driver)
    menu.select_level_Menu("中控调度,作业任务汇报")
    task_report = WorkTaskReport(driver)
    task_report.search(input)
    task_report.report(input)
    task_report.check_table_task(input)


@allure.story('一、卸船流程')
@allure.title('12.装卸船作业票-中控')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(), 'unship.yaml')))
def test_job_slip_control(driver, input):
    menu = Menu(driver)
    menu.select_level_Menu("计件工资,装卸船作业票,装卸船作业票-中控")
    job_slip = JobSlipControl(driver)
    job_slip.search(input)
    job_slip.generate()
    job_slip.check_table(input)
    job_slip.audit()


@allure.story('一、卸船流程')
@allure.title('12.装卸船作业票-人事')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(), 'unship.yaml')))
def test_job_slip_personnel(driver, input):
    menu = Menu(driver)
    menu.select_level_Menu("计件工资,装卸船作业票,装卸船作业票-人事")
    personnel = JobSlipPersonnel(driver)
    personnel.search(input)
    personnel.audit()
    time.sleep(1)
    personnel.check_table(input)