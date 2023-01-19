import os
import allure
import pytest as pytest
from Commons.Controls.tag import Tag
from Commons.yamlread import read_yaml
from GTOS.Config import config
from GTOS.PageObject.Control_Ship.No_Structure_Monitoring import NO_Structure_Monitoring
from GTOS.PageObject.DataManagement.ExitInformation_manifest import Manifest
from GTOS.PageObject.Mechanical_Control.Job_Order_Monitoring import Job_Order_Monitoring
from GTOS.PageObject.Ship_Planning.No_Structure_Stowage import No_Structure_Stowage
from GTOS.PageObject.gtos_menu import GtosMenu

@pytest.mark.skip
@allure.story('5.装船流程')
@allure.title('1.装船箱放行')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(),'05_PutBoxIntoShipProcess','loadship.yaml')))
def testCheckInBox(driver,input):
    menu = GtosMenu(driver)
    menu.select_level_Menu("资料管理,出口资料，装船箱放行")
    Load=Manifest(driver)
    Load.search(input)
    Load.permitthrough(input)

@allure.story('5.装船流程')
@allure.title('2.无结构船舶配载')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(),'05_PutBoxIntoShipProcess','loadship.yaml')))
def testship_stowage(driver, input):
    """无结构配载"""
    menu = GtosMenu(driver)
    menu.select_level_Menu("船舶策划,无结构船舶配载")
    stowage = No_Structure_Stowage(driver)
    stowage.search(input)
    stowage.check(input)
    stowage.stowage()

@allure.story('5.装船流程')
@allure.title('3.无结构船舶监控')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(),'05_PutBoxIntoShipProcess','loadship.yaml')))
def testship_monitor(driver, input):
    """无结构船舶监控"""
    menu = GtosMenu(driver)
    menu.select_level_Menu("船舶监控,无结构船舶监控")
    Monitor = NO_Structure_Monitoring(driver)
    Monitor.Retrieve(input)
    Monitor.clickLadeShipTag()
    Monitor.LadeShip_check_values(input)
    Monitor.LadeShip_Send_Box()
@allure.story('5.装船流程')
@allure.title('4.作业指令监控')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(),'05_PutBoxIntoShipProcess','loadship.yaml')))
def testship_order(driver, input):
    """作业指令监控"""
    menu = GtosMenu(driver)
    menu.select_level_Menu("机械控制,作业指令监控")
    work = Job_Order_Monitoring(driver)
    work.Retrieve(input,config.outBoxNumber)
    work.order_info_check(input)
    work.charge_car("C305")
    work.send_box(input)
    work.LadeShip_confirm(input)
    Tag(driver).closeChoiceTag('作业指令监控')

if __name__ == '__main__':
    #pytest.main(['-vs'])
    pytest.main(['-s', '-v', 'testEnterBoxProcess.py','--html=../report/report.html', '--alluredir','../report/allure-results'])