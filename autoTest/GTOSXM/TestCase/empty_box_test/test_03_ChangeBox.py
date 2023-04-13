import os
import time
import allure
import pytest
from Commons.Controls.tag import Tag
from GTOSXM.Config import config, configinterface
from GTOSXM.PageObject.CrossingManagement.Incoming_job_list import Incoming_job_list
from GTOSXM.PageObject.CrossingManagement.carOut import Car_Out
from GTOSXM.PageObject.DataManagement.Box_Cargo_Synthesize import Box_Cargo_Synthesize
from GTOSXM.PageObject.Mechanical_Control.Job_Order_Monitoring import Job_Order_Monitoring
from GTOSXM.PageObject.Yard_Planning.Empty_Box_Dredge_Monitor import Empty_Box_Dredge_Monitor
from GTOSXM.PageObject.gtos_menu import GtosMenu
from GTOSXM.PageObject.Yard_Planning.Empty_Box_Dredge_Plan import Empty_Box_Dredge_Plan
from Commons.yamlread import read_yaml
from GTOSXM.TestCase.empty_box_test.InterfacePage import Interface


# @pytest.mark.skipif
@allure.story('1.新增计划')
@allure.title('1、空箱输运计划-换箱')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(), '01.yaml')))
def testImmediatePlan(driver, input):
    """新增空箱输运计划"""
    print("******************************************Smoke Test Start***********************************************")
    menu = GtosMenu(driver)
    menu.select_level_Menu("堆场策划,空箱,安排空箱疏运计划")
    plan = Empty_Box_Dredge_Plan(driver)
    plan.addplan()
    plan.input_values('码头选箱', input)
    Tag(driver).closeTagGtos('安排空箱疏运计划')


# @pytest.mark.skipif
@allure.story('2.监控开启情况')
@allure.title('1、空箱输运计划-换箱')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(), '01.yaml')))
def testmonitorswitch(driver, input):
    """空箱疏运监控开启"""
    menu = GtosMenu(driver)
    menu.select_level_Menu("堆场策划,空箱,空箱疏运监控")
    monitor = Empty_Box_Dredge_Monitor(driver)
    monitor.monitor_switch()
    Tag(driver).closeTagGtos('空箱疏运监控')

# @pytest.mark.skipif
@allure.story('3.RPS接口，工作指令发箱')
@allure.title('1、空箱输运计划-换箱')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(), 'changebox_process.yaml')))
def testJob(driver, input):
    """接口-智能道口-RPS """
    menu = GtosMenu(driver)
    htps = Interface(driver)
    htps.interface_login()
    htps.Intelligent_crossing()
    menu.select_level_Menu("机械控制,作业指令监控")
    charge_car = Job_Order_Monitoring(driver)
    charge_car.Retrieve(input, config.importNumber, configinterface.boxNumber)
    charge_car.dredge_check(configinterface.boxNumber)
    charge_car.send_box(input)
    Tag(driver).closeTagGtos('作业指令监控')

# @pytest.mark.skipif
@allure.story('4.换箱操作')
@allure.title('1、空箱输运计划-换箱')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(), 'changebox_process.yaml')))
def testChangeBox(driver, input):
    """换箱操作"""
    menu = GtosMenu(driver)
    menu.select_level_Menu("道口管理,进场作业列表")
    incoming = Incoming_job_list(driver)
    incoming.input_values(configinterface.boxNumber)
    incoming.check_second()
    incoming.refund_box()
    Tag(driver).closeTagGtos('进场作业列表')


# @pytest.mark.skipif
@allure.story('5.工作指令换箱，堆场操作')
@allure.title('1、空箱输运计划-换箱')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(), 'changebox_process.yaml')))
def testJobDoing(driver, input):
    """作业指令监控"""
    menu = GtosMenu(driver)
    menu.select_level_Menu("机械控制,作业指令监控")
    charge_car = Job_Order_Monitoring(driver)
    charge_car.Retrieve(input, carnumber='闽D55119')
    charge_car.selectRow_check(configinterface.boxNumbertwo)
    charge_car.selectRow_check(configinterface.boxNumber)
    charge_car.closed_box(input)
    charge_car.dredge_check(configinterface.boxNumbertwo)
    charge_car.send_box(input)
    Tag(driver).closeTagGtos('作业指令监控')

# @pytest.mark.skipif
@allure.story('6.车辆出场')
@allure.title('1、空箱输运计划-换箱')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(), 'discharging_process.yaml')))
def testCar_Out(driver, input):
    """车辆出场"""
    menu = GtosMenu(driver)
    menu.select_level_Menu("道口管理,车辆出场")
    car_out = Car_Out(driver)
    car_out.input_values(input)
    car_out.retrieve()
    car_out.confirm_out_picking()
    Tag(driver).closeTagGtos('车辆出场')

# @pytest.mark.skipif
@allure.story('7.查看箱状态')
@allure.title('1、空箱输运计划-换箱')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(), 'discharging_process.yaml')))
def testBox_state(driver, input):
    """查看箱状态"""
    menu = GtosMenu(driver)
    menu.select_level_Menu("资料管理,信息查询,箱货综合查询")
    Box_state = Box_Cargo_Synthesize(driver)
    Box_state.input_values()
    Tag(driver).closeTagGtos('箱货综合查询')

if __name__ == '__main__':
    pytest.main(['-sv'])
