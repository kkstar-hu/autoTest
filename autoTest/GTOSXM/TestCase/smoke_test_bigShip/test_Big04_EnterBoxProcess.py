import os
import allure
import pytest as pytest
from Commons.Controls.tag import Tag
from Commons.yamlread import read_yaml
from GTOSXM.Config import config
from GTOSXM.PageObject.CrossingManagement.carOut import Car_Out
from GTOSXM.PageObject.CrossingManagement.checkInBox import CheckInBox
from GTOSXM.PageObject.Mechanical_Control.Job_Order_Monitoring import Job_Order_Monitoring
from GTOSXM.PageObject.gtos_menu import GtosMenu


@allure.story('4.大船新增进箱计划')
@allure.title('1.进箱流程')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(), '04_EnterBoxProcess', 'inboxplan.yaml')))
def testCheckInBox(driver, input):
    menu = GtosMenu(driver)
    menu.select_level_Menu("道口管理,办理进箱手续V1")
    checkInBox = CheckInBox(driver)
    checkInBox.search(input, config.outBoxNumber)
    checkInBox.input_checkin_info(input)
    checkInBox.addgoodsinfo(input, config.outBoxNumber)
    checkInBox.input_info(input)
    checkInBox.confirm_button(input)
    Tag(driver).closeTagGtos('办理进箱手续V1')


@allure.story('4.大船新增进箱计划')
@allure.title('3.堆场收箱')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(), '04_EnterBoxProcess', 'inboxplan.yaml')))
def testReceive_box(driver, input):
    """工作指令-堆场收箱"""
    menu = GtosMenu(driver)
    menu.select_level_Menu("机械控制,作业指令监控")
    work = Job_Order_Monitoring(driver)
    work.Retrieve(input, config.outportNumber, config.outBoxNumber)
    work.order_info_check(input, config.outBoxNumber)
    work.closed_box(input)
    Tag(driver).closeTagGtos('作业指令监控')


@allure.story('4.大船新增进箱计划')
@allure.title('4.车辆出场')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(), '04_EnterBoxProcess', 'inboxplan.yaml')))
def testCar_Out(driver, input):
    menu = GtosMenu(driver)
    menu.select_level_Menu("道口管理,车辆出场")
    car_out = Car_Out(driver)
    car_out.input_values(input)
    car_out.retrieve()
    car_out.confirm_out_loadingAndLifting()
    Tag(driver).closeTagGtos('车辆出场')


