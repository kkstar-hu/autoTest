import os

import allure
import pytest
from Commons.Controls.tag import Tag
from GTOSXM.Config import config
from GTOSXM.PageObject.CrossingManagement.checkOutBox import CheckOutBox
from GTOSXM.PageObject.Mechanical_Control.Job_Order_Monitoring import Job_Order_Monitoring
from GTOSXM.PageObject.gtos_menu import GtosMenu
from Commons.yamlread import read_yaml
from GTOSXM.PageObject.Acceptance_Plan.Pick_up_Acceptance import Packing_up
from GTOSXM.PageObject.Acceptance_Plan.Planmanagement import PlanManagement
from GTOSXM.PageObject.CrossingManagement.carOut import Car_Out


# @pytest.mark.skipif
# @pytest.mark.parametrize("input", read_yaml('packing_process.yaml'))
@allure.title('1、新增提箱计划')
@allure.story('3.提箱流程')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(),'03_PackingProcess', 'packing_process.yaml')))
def testPacking(driver,input):
    """提箱受理"""
    menu = GtosMenu(driver)
    menu.select_level_Menu("计划受理,安排计划,提箱受理")
    packing = Packing_up(driver)
    packing.packing_process(input,config.boxNumber)
    Tag(driver).closeTagGtos('提箱受理')

# @pytest.mark.skipif
# # @pytest.mark.parametrize("input", read_yaml('packing_process.yaml'))
# @allure.title('2、获取箱预约号')
# @allure.story('3.提箱流程')
# @pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(),'03_PackingProcess', 'packing_process.yaml')))
# def testPackingManagement(driver,input):
#     """计划管理--获取箱预约号"""
#     menu = GtosMenu(driver)
#     menu.select_level_Menu("计划受理,计划管理")
#     planmanegement = PlanManagement(driver)
#     planmanegement.process(config.boxNumber)
#     Tag(driver).closeTagGtos('计划管理')

# @pytest.mark.skipif
# @pytest.mark.parametrize("input", read_yaml('packing_process.yaml'))
@allure.title('2、办理提箱手续')
@allure.story('3.提箱流程')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(),'03_PackingProcess', 'packing_process.yaml')))
def testCheckOutBox(driver,input):
    """办理提箱手续"""
    menu = GtosMenu(driver)
    menu.select_level_Menu("道口管理,办理提箱手续V1")
    checkoutbox = CheckOutBox(driver)
    checkoutbox.process(input)
    Tag(driver).closeTagGtos('办理提箱手续V1')

# @pytest.mark.skipif
# @pytest.mark.parametrize("input", read_yaml('packing_process.yaml'))
@allure.title('3、工作指令堆场发箱')
@allure.story('3.提箱流程')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(),'03_PackingProcess', 'packing_process.yaml')))
def testSend_box(driver, input):
    """工作指令-堆场发箱"""
    menu = GtosMenu(driver)
    menu.select_level_Menu("机械控制,作业指令监控")
    charge_car = Job_Order_Monitoring(driver)
    charge_car.Job_SendBoxOrder(input,config.importNumber,config.boxNumber)
    Tag(driver).closeTagGtos('作业指令监控')

# @pytest.mark.skipif
# @pytest.mark.parametrize("input", read_yaml('packing_process.yaml'))
@allure.title('4、车辆出场')
@allure.story('3.提箱流程')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(),'03_PackingProcess', 'packing_process.yaml')))
def testCar_Out(driver, input):
    """工作指令-堆场发箱"""
    menu = GtosMenu(driver)
    menu.select_level_Menu("道口管理,车辆出场")
    car_out = Car_Out(driver)
    car_out.process(input,config.boxNumber)
    Tag(driver).closeChoiceTag('车辆出场')



if __name__ == '__main__':
    pytest.main(['-sv'])