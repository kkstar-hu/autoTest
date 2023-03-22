import os
import allure
from Commons.Controls.tag import Tag
from Commons.menu import Menu
from Commons.yamlread import read_yaml
from NZYMS.Config import config
from NZYMS.PageObject.CenterControlManagement.car_load import Car_Load
from NZYMS.PageObject.CrossingManagement.Mention_Box_registration import Mention_Box_registration
from NZYMS.PageObject.CrossingManagement.Out_confirm import Out_Confirm
from NZYMS.PageObject.BoxManagement.outPlan import Out_Plan
import pytest as pytest


@allure.title('1.新增出场计划')
@allure.story('10、出场计划流程')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(), '06_outboxprocess', 'stor_box.yaml')))
def testOut_Plan(driver, input):
    """出场计划"""
    menu = Menu(driver)
    menu.select_level_Menu("箱务管理,出场计划")
    outplan = Out_Plan(driver)
    outplan.addPlan(input)


@allure.title('2.新增箱子信息和货信息')
@allure.story('10、出场计划流程')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(), '06_outboxprocess', 'stor_box.yaml')))
def testOut_PlanAddbox(driver, input):
    outplan = Out_Plan(driver)
    outplan.addBoxPlan(input)
    outplan.pay_for_box(input)
    Tag(driver).closeTag("出场计划")

@allure.title('3.提箱进场登记')
@allure.story('10、出场计划流程')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(), '06_outboxprocess', 'stor_box.yaml')))
def testMention_Box_registration(driver,input):
    """提箱进场登记"""
    menu = Menu(driver)
    menu.select_level_Menu("道口管理,提箱进场登记")
    out_box = Mention_Box_registration(driver)
    out_box.select_values(input)
    out_box.mention_box_plan(input)
    out_box.confirm_button(input)
    Tag(driver).closeTag("提箱进场登记")

@allure.title('4.车载提箱')
@allure.story('10、出场计划流程')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(), '06_outboxprocess', 'stor_box.yaml')))
def testSend_Box_Load(driver, input):
    """车载操作"""
    menu = Menu(driver)
    menu.select_level_Menu("中控管理,车载")
    #进人新窗口页面工作
    cls = driver.window_handles
    driver.switch_to.window(cls[1])
    car = Car_Load(driver)
    car.findCommand(input)
    car.choice_car(config.boxNumberOutPlan)
    car.container_Box(input)

@allure.title('5.车辆出场')
@allure.story('10、出场计划流程')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(), '06_outboxprocess', 'stor_box.yaml')))
def testSend_Box_Out_Confirm(driver, input):
    """车辆出场"""
    cls = driver.window_handles
    driver.switch_to.window(cls[0])
    menu = Menu(driver)
    menu.select_level_Menu("道口管理,出场确认")
    out_confirm = Out_Confirm(driver)
    out_confirm.out_confirm(input)
    out_confirm.choice_car(input)
    out_confirm.confirm_button()
    Tag(driver).closeTag("出场确认")


