import os
import time
import allure
import pytest
from BTOSLJ.PageObject.business_accept.domestic_trade_accept_goods import DomesticTradeAcceptGoods
from BTOSLJ.PageObject.center_control.job_task import JobTask
from BTOSLJ.PageObject.center_control.work_task import WorkTask
from BTOSLJ.PageObject.center_control.work_task_report import WorkTaskReport
from BTOSLJ.PageObject.crossing_management.in_cross import InCross
from BTOSLJ.PageObject.crossing_management.out_cross import OutCross
from BTOSLJ.PageObject.piece_wage.car_work_men import CarWorkMen
from BTOSLJ.PageObject.piece_wage.car_work_store import CarWorkStore
from BTOSLJ.PageObject.plan_management.carship_workplan import CarShipWorkPlan
from Commons.Controls.tag import Tag
from Commons.menu import Menu
from Commons.yamlread import read_yaml


@allure.story('二、内贸提货流程')
@allure.title('1.新增内贸提货受理')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(), '03_acceptgoods.yaml')))
def test_add_store_bill(driver, input):
    menu = Menu(driver)
    menu.select_level_Menu("业务受理,提货受理,内贸提货受理")
    accept_goods = DomesticTradeAcceptGoods(driver)
    accept_goods.add_acceptance_information(input)
    time.sleep(0.5)
    accept_goods.check_table_bill(input)
    accept_goods.click_next_button()
    accept_goods.deal_acceptance_information(input)
    Tag(driver).closeTag("内贸提货受理")


@allure.story('二、内贸提货流程')
@allure.title('2.新增车驳作业计划')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(), '03_acceptgoods.yaml')))
def test_add_work_plan(driver, input):
    menu = Menu(driver)
    menu.select_level_Menu("计划管理,车驳作业计划")
    car_work_plan = CarShipWorkPlan(driver)
    car_work_plan.search()
    car_work_plan.add_plan(input)
    Tag(driver).closeTag("车驳作业计划")


@allure.story('二、内贸提货流程')
@allure.title('3.当班作业任务-安排作业路')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(), '03_acceptgoods.yaml')))
def test_add_work_task(driver, input):
    menu = Menu(driver)
    menu.select_level_Menu("中控调度,当班作业任务")
    work_task = WorkTask(driver)
    work_task.search(input)
    work_task.add_plan(input)
    work_task.car_work(input)
    time.sleep(0.5)
    work_task.check_table_task(input)
    Tag(driver).closeTag("当班作业任务")


@allure.story('二、内贸提货流程')
@allure.title('4.进门道口管理')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(), '03_acceptgoods.yaml')))
def test_in_cross(driver, input):
    menu = Menu(driver)
    menu.select_level_Menu("道口管理,进门道口管理")
    cross = InCross(driver)
    cross.check()
    time.sleep(0.5)
    Tag(driver).closeTag("进门道口管理")


@allure.story('二、内贸提货流程')
@allure.title('5.理货员安排')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(), '03_acceptgoods.yaml')))
def test_tallyman_arrange(driver, input):
    menu = Menu(driver)
    menu.select_level_Menu("中控调度,作业任务管理")
    tallyman = JobTask(driver)
    tallyman.search(input)
    tallyman.check_car_task(input)
    tallyman.arrange_tallyman(input)


@allure.story('二、内贸提货流程')
@allure.title('6.库场安排')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(), '03_acceptgoods.yaml')))
def test_mechanical_arrange(driver, input):
    menu = Menu(driver)
    menu.select_level_Menu("中控调度,作业任务管理")
    mechanical = JobTask(driver)
    mechanical.search(input)
    mechanical.select_row_accept_number()
    mechanical.arrange_warehouse(input)


@allure.story('二、内贸提货流程')
@allure.title('7.作业票汇报配置')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(), '03_acceptgoods.yaml')))
def test_report_config(driver, input):
    menu = Menu(driver)
    menu.select_level_Menu("中控调度,作业任务管理")
    report_config = JobTask(driver)
    report_config.search(input)
    report_config.select_row_accept_number()
    report_config.report_config(input)
    report_config.labor_team_config(input)
    Tag(driver).closeTag("作业任务管理")


@allure.story('二、内贸提货流程')
@allure.title('8.理货汇报')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(), '03_acceptgoods.yaml')))
def test_task_report(driver, input):
    menu = Menu(driver)
    menu.select_level_Menu("中控调度,作业任务汇报")
    task_report = WorkTaskReport(driver)
    task_report.search(input)
    task_report.select_row_accept_number()
    task_report.report(input)
    task_report.check_table_task(input)
    task_report.audit_report()
    task_report.audit_task()
    Tag(driver).closeTag("作业任务汇报")


@allure.story('二、内贸提货流程')
@allure.title('9.车驳库作业票-仓库')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(), '03_acceptgoods.yaml')))
def test_job_slip_control(driver, input):
    menu = Menu(driver)
    menu.select_level_Menu("计件工资,车驳库场作业票,车驳库作业票-仓库")
    car_work = CarWorkStore(driver)
    car_work.search(input)
    car_work.generate()
    car_work.audit()
    car_work.check_table(input)
    Tag(driver).closeTag("车驳库作业票-仓库")


@allure.story('二、内贸提货流程')
@allure.title('10.车驳库作业票-人事')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(), '03_acceptgoods.yaml')))
def test_job_slip_personnel(driver, input):
    menu = Menu(driver)
    menu.select_level_Menu("计件工资,车驳库场作业票,车驳库作业票-人事")
    personnel = CarWorkMen(driver)
    personnel.search(input)
    personnel.edit(input)
    time.sleep(1)
    personnel.check_table(input)
    Tag(driver).closeTag("车驳库作业票-人事")


@allure.story('二、内贸提货流程')
@allure.title('11.出门道口管理')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(), '03_acceptgoods.yaml')))
def test_out(driver, input):
    menu = Menu(driver)
    menu.select_level_Menu("道口管理,出门道口管理")
    cross = OutCross(driver)
    cross.search()
    cross.out(input)
    Tag(driver).closeTag("出门道口管理")

