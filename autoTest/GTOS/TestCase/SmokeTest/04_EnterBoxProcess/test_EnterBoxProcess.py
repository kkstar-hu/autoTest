import os
import allure
import pytest as pytest
from Commons.Controls.tag import Tag
from Commons.RandomFunction import CommonGenerator
from Commons.yamlread import read_yaml
from GTOS.Config import config
from GTOS.Config.config import takeNumber
from GTOS.PageObject.CrossingManagement.carOut import Car_Out
from GTOS.PageObject.CrossingManagement.checkInBox import CheckInBox
from GTOS.PageObject.Mechanical_Control.Job_Order_Monitoring import Job_Order_Monitoring
from GTOS.PageObject.gtos_menu import GtosMenu


@allure.story('4.新增进箱计划')
@allure.title('1.进箱流程')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(),'04_EnterBoxProcess','checkInBox.yaml')))
def testCheckInBox(driver,input):
    menu = GtosMenu(driver)
    menu.select_level_Menu("道口管理,办理进箱手续V1")
    checkInBox = CheckInBox(driver)
    checkInBox.search(input,config.outBoxNumber)
    checkInBox.input_checkin_info(input)
    checkInBox.addgoodsinfo(input,takeNumber)
    checkInBox.input_info(input)
    checkInBox.confirm_button(input)
    Tag(driver).closeTagGtos('办理进箱手续V1')

@allure.story('4.新增进箱计划')
@allure.title('2.堆场收箱')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(),'04_EnterBoxProcess','checkInBox.yaml')))
def testReceive_box(driver, input):
    """工作指令-堆场收箱"""
    menu = GtosMenu(driver)
    menu.select_level_Menu("机械控制,作业指令监控")
    work = Job_Order_Monitoring(driver)
    work.Retrieve(input,config.outportNumber)
    work.order_info_check(input,config.outBoxNumber)
    work.closed_box(input)
    Tag(driver).closeTagGtos('作业指令监控')


@allure.story('4.新增进箱计划')
@allure.title('3.车辆出场')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(),'04_EnterBoxProcess','checkInBox.yaml')))
def testCar_Out(driver, input):
    menu = GtosMenu(driver)
    menu.select_level_Menu("道口管理,车辆出场")
    car_out = Car_Out(driver)
    car_out.process_loading(input,config.outBoxNumber)
    Tag(driver).closeTagGtos('车辆出场')


if __name__ == '__main__':
    #pytest.main(['-vs'])
    pytest.main(['-s', '-v', 'test_EnterBoxProcess.py','--html=../report/report.html', '--alluredir','../report/allure-results'])