import os
import time

import allure
import pytest
from BTOSLJ.Config import config
from BTOSLJ.PageObject.center_control.job_task import JobTask
from BTOSLJ.PageObject.center_control.mechanical_attendance import MechanicalAttendance
from BTOSLJ.PageObject.center_control.work_task import WorkTask
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
def test_mechanical_arrange(driver, input):
    menu = Menu(driver)
    menu.select_level_Menu("中控调度,机械出勤")
    mechanical = MechanicalAttendance(driver)
    mechanical.search(input)
    mechanical.arrange_mechanical(input)

