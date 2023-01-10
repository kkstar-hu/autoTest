import os

import allure
import pytest as pytest

from Base.basepage import BasePage
from Commons.Controls.tag import Tag
from Commons.yamlread import read_yaml, generate_yaml,generate_yaml_gtos
import pytest_check as check

from GTOS.Config import config
from GTOS.Controls.Gtos_table import Gtos_table
from GTOS.Controls.text import Gtos_text
from GTOS.PageObject.Control_Ship.No_Structure_Monitoring import NO_Structure_Monitoring
from GTOS.PageObject.CrossingManagement.carOut import Car_Out
from GTOS.PageObject.CrossingManagement.checkInBox import CheckInBox
from GTOS.PageObject.DataManagement.ExitInformation_manifest import Manifest
from GTOS.PageObject.Mechanical_Control.Job_Order_Monitoring import Job_Order_Monitoring
from GTOS.PageObject.Ship_Planning.No_Structure_Stowage import No_Structure_Stowage
from GTOS.PageObject.gtos_menu import GtosMenu

@pytest.mark.skip
@allure.story('1.装船流程')
@allure.title('1.装船箱放行')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(),'loadship.yaml')))
def testCheckInBox(driver,input):
    menu = GtosMenu(driver)
    menu.select_level_Menu("资料管理,出口资料，装船箱放行")
    Load=Manifest(driver)
    Load.search(input)
    Load.permitthrough(input)
@pytest.mark.skip
@allure.story('1.装船流程')
@allure.title('1.无结构船舶配载')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(),'loadship.yaml')))
def testship_stowage(driver, input):
    """无结构配载"""
    menu = GtosMenu(driver)
    menu.select_level_Menu("船舶策划,无结构船舶配载")
    stowage = No_Structure_Stowage(driver)
    stowage.search(input)
    stowage.check(input)
    stowage.stowage()

@pytest.mark.skip
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(),'loadship.yaml')))
def testship_monitor(driver, input):
    """无结构船舶监控"""
    menu = GtosMenu(driver)
    menu.select_level_Menu("船舶监控,无结构船舶监控")
    Monitor = NO_Structure_Monitoring(driver)
    Monitor.Retrieve(input)
    Monitor.clickLadeShipTag()
    Monitor.LadeShip_check_values(input)
    Monitor.LadeShip_Send_Box()

@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(),'loadship.yaml')))
def testship_order(driver, input):
    """作业指令监控"""
    menu = GtosMenu(driver)
    menu.select_level_Menu("机械控制,作业指令监控")
    work = Job_Order_Monitoring(driver)
    work.Retrieve(input,config.boxNumber)
    work.order_info_check(input)
    #work.charge_car("C305")
    #work.send_box(input)
    work.LadeShip_confirm(input)
    Tag(driver).closeChoiceTag('作业指令监控')

if __name__ == '__main__':
    #pytest.main(['-vs'])
    pytest.main(['-s', '-v', 'testEnterBoxProcess.py','--html=../report/report.html', '--alluredir','../report/allure-results'])