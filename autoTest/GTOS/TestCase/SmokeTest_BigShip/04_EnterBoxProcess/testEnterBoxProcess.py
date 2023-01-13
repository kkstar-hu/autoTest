import os
import allure
import pytest as pytest
from Commons.Controls.tag import Tag
from Commons.yamlread import read_yaml
from GTOS.Config import config
from GTOS.PageObject.CrossingManagement.carOut import Car_Out
from GTOS.PageObject.CrossingManagement.checkInBox import CheckInBox
from GTOS.PageObject.Mechanical_Control.Job_Order_Monitoring import Job_Order_Monitoring
from GTOS.PageObject.gtos_menu import GtosMenu


@allure.story('1.进箱流程')
@allure.title('4.新增进箱计划')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(),'checkInBox.yaml')))
def testCheckInBox(driver,input):
    menu = GtosMenu(driver)
    menu.select_level_Menu("道口管理,办理进箱手续V1")
    checkInBox = CheckInBox(driver)
    checkInBox.search(input,config.boxNumber)
    checkInBox.input_checkin_info(input)
    checkInBox.addgoodsinfo(input,config.takeNumber)
    checkInBox.input_info(input)
    checkInBox.confirm_button(input)

@allure.story('2.堆场收箱')
@allure.title('4.新增进箱计划')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(),'checkInBox.yaml')))
def testReceive_box(driver, input):
    """工作指令-堆场收箱"""
    menu = GtosMenu(driver)
    menu.select_level_Menu("机械控制,作业指令监控")
    work = Job_Order_Monitoring(driver)
    work.Retrieve(input,config.boxNumber)
    work.order_info_check(input)
    work.closed_box(input)
    Tag(driver).closeChoiceTag('作业指令监控')


@allure.story('3.车辆出场')
@allure.title('4.新增进箱计划')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(),'checkInBox.yaml')))
def testCar_Out(driver, input):
    menu = GtosMenu(driver)
    menu.select_level_Menu("道口管理,车辆出场")
    car_out = Car_Out(driver)
    car_out.process_loading(input)
    Tag(driver).closeChoiceTag('车辆出场')


if __name__ == '__main__':
    #pytest.main(['-vs'])
    pytest.main(['-s', '-v', 'testEnterBoxProcess.py','--html=../report/report.html', '--alluredir','../report/allure-results'])