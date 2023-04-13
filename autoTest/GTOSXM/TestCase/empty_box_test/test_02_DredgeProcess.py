import os
import time
import allure
import pytest
from Commons.Controls.tag import Tag
from GTOSXM.Config import configinterface
from GTOSXM.PageObject.CrossingManagement.Incoming_job_list import Incoming_job_list
from GTOSXM.PageObject.CrossingManagement.carOut import Car_Out
from GTOSXM.PageObject.Yard_Planning.Empty_Box_Dredge_Monitor import Empty_Box_Dredge_Monitor
from GTOSXM.PageObject.gtos_menu import GtosMenu
from GTOSXM.PageObject.Yard_Planning.Empty_Box_Dredge_Plan import Empty_Box_Dredge_Plan
from Commons.yamlread import read_yaml
from GTOSXM.TestCase.empty_box_test.InterfacePage import Interface


# @pytest.mark.skipif
@allure.story('1.新增计划')
@allure.title('1、空箱输运计划')
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
@allure.title('1、空箱输运计划')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(), '01.yaml')))
def testmonitorswitch(driver, input):
    """空箱疏运监控开启"""
    menu = GtosMenu(driver)
    menu.select_level_Menu("堆场策划,空箱,空箱疏运监控")
    monitor = Empty_Box_Dredge_Monitor(driver)
    monitor.monitor_switch()
    Tag(driver).closeTagGtos('空箱疏运监控')


# @pytest.mark.skipif
@allure.story('3.RPS接口发箱，工作指令查看结果')
@allure.title('1、空箱输运计划')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(), 'discharging_process.yaml')))
def testJob(driver, input):
    """接口-智能道口-RPS-查看"""
    menu = GtosMenu(driver)
    htps = Interface(driver)
    menu.select_level_Menu("道口管理,进场作业列表")
    incoming = Incoming_job_list(driver)
    htps.interface_login()
    htps.Intelligent_crossing()
    incoming.input_values(configinterface.boxNumber)
    incoming.check_first()
    htps.RPSAreaBayList()
    htps.RPSBayInfo()
    htps.RPSSend()
    time.sleep(1)
    incoming.check_second()
    Tag(driver).closeTagGtos('进场作业列表')


# @pytest.mark.skipif
@allure.story('4.车辆出场')
@allure.title('1、空箱输运计划')
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


if __name__ == '__main__':
    pytest.main(['-sv'])
