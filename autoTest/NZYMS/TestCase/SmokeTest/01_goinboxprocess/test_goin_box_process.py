import os

import allure

from Commons.Controls.tag import Tag
from Commons.menu import Menu
from Commons.yamlread import read_yaml
from NZYMS.Config import config
from NZYMS.PageObject.BoxManagement.goInPlan_BoxNumber import GoInPlan_BoxNumber
from NZYMS.PageObject.CenterControlManagement.car_load import Car_Load
from NZYMS.PageObject.CrossingManagement.Out_confirm import Out_Confirm
from NZYMS.PageObject.CrossingManagement.Send_Box_registration import Send_Box_registration
from NZYMS.PageObject.CrossingManagement.storePlan import StorePlan
import pytest as pytest


#@pytest.mark.skip
@allure.story('1.进箱计划流程')
@allure.title('1.新增进箱计划')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(),'01_goinboxprocess','goInPlan_BoxNumber.yaml')))
def testAddGoInPlan_BoxNumber(driver, input):
    menu=Menu(driver)
    menu.select_level_Menu("箱务管理,进场计划(按箱号)")
    goInPlan=GoInPlan_BoxNumber(driver)
    goInPlan.addPlan(input)

#@pytest.mark.skip
@allure.title('2.新增计划箱和箱信息')
@allure.story('1.进箱计划流程')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(),'01_goinboxprocess','boxPlan.yaml')))
def testAddBox(driver, input):
    boxPlan = GoInPlan_BoxNumber(driver)
    boxPlan.addBoxPlan(input,config.boxNumber)
    boxPlan.addBoxInformation(input)
    boxPlan.addBoxPlan(input, config.boxNumberOutPlan)
    boxPlan.addBoxInformation(input)
    boxPlan.clickExcute(1)
    Tag(driver).closeTag("进场计划(按箱号)")


# @pytest.mark.skip
@allure.title('3.添加堆存计划')
@allure.story('1.进箱计划流程')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(),'01_goinboxprocess','storePlan.yaml')))
def testAddStorePlan(driver, input):
    menu = Menu(driver)
    menu.select_level_Menu("中控管理,场内计划管理,堆存计划")
    storePlan = StorePlan(driver)
    storePlan.addStoreArea(input)
    Tag(driver).closeTag("堆存计划")

# @pytest.mark.skip
@allure.title('4.送箱进场登记')
@allure.story('1.进箱计划流程')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(),'01_goinboxprocess','Send_Bos_Plan.yaml')))
def testSend_Box_Plan(driver, input):
    """送箱进场登记有计划"""
    menu = Menu(driver)
    menu.select_level_Menu("道口管理,送箱进场登记")
    send_box = Send_Box_registration(driver)
    send_box.select_values(input)
    send_box.send_box_plan(input,config.boxNumber)
    send_box.add_box()
    send_box.send_box_plan(input,config.boxNumberOutPlan)
    send_box.confirm_button(input)
    Tag(driver).closeTag("送箱进场登记")

#@pytest.mark.skip
@allure.title('5.车载落箱')
@allure.story('1.进箱计划流程')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(),'01_goinboxprocess','car_load.yaml')))
def testSend_Box_Load(driver, input):
    """车载操作"""
    menu = Menu(driver)
    menu.select_level_Menu("中控管理,车载")
    #进人新窗口页面工作
    cls = driver.window_handles
    driver.switch_to.window(cls[1])
    car = Car_Load(driver)
    car.type_of_job(input)
    car.choice_car(config.boxNumber)
    car.place_box()
    car.choice_car(config.boxNumberOutPlan)
    car.place_box()
    driver.close()


@allure.title('6.车辆出场')
@allure.story('1.进箱计划流程')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(),'01_goinboxprocess','car_load.yaml')))
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




if __name__ == '__main__':
    pytest.main(['-vs'])
    # pytest.main(['-s', '-v', 'test_goin_box_process.py','--html=../report/report.html', '--alluredir','../report/allure-results'])
    # os.system('./report.html -o ./report/html --clean')