import os
import allure
import pytest as pytest
from Commons.Controls.tag import Tag
from Commons.yamlread import read_yaml
from GTOSXM.Config import config
from GTOSXM.PageObject.Control_Ship.No_Structure_Monitoring import NO_Structure_Monitoring
from GTOSXM.PageObject.DataManagement.ExitInformation_manifest import Manifest
from GTOSXM.PageObject.Mechanical_Control.Inset_Car import Inset_Car
from GTOSXM.PageObject.Mechanical_Control.Job_Order_Monitoring import Job_Order_Monitoring
from GTOSXM.PageObject.Ship_Planning.No_Structure_Stowage import No_Structure_Stowage
from GTOSXM.PageObject.gtos_menu import GtosMenu

# @pytest.mark.skip
@allure.story('5.装船流程')
@allure.title('1.装船箱放行')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(),'05_PutBoxIntoShipProcess','loadship.yaml')))
def testCheckInBox(driver,input):
    menu = GtosMenu(driver)
    menu.select_level_Menu("资料管理,出口资料,装船箱放行")
    Load=Manifest(driver)
    Load.search()
    Load.permitthrough()

# @pytest.mark.skip
@allure.story('5.装船流程')
@allure.title('2.无结构船舶配载')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(),'05_PutBoxIntoShipProcess','loadship.yaml')))
def testship_stowage(driver, input):
    """无结构配载"""
    menu = GtosMenu(driver)
    menu.select_level_Menu("船舶策划,无结构船舶配载")
    stowage = No_Structure_Stowage(driver)
    stowage.search()
    stowage.check(input,config.outBoxNumber)
    stowage.stowage(config.outBoxNumber)
    Tag(driver).closeTagGtos('无结构船舶配载')



@allure.title('3、内集卡控制')
@allure.story('5.装船流程')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(),'05_PutBoxIntoShipProcess','loadship.yaml')))
def testCharge_Car(driver, input):
    """查看内集卡"""
    menu = GtosMenu(driver)
    menu.select_level_Menu("机械控制,内集卡控制")
    inset_car = Inset_Car(driver)
    inset_car.choice_job('ALL')
    inset_car.choice_cars('作业步骤','空车')
    Tag(driver).closeTagGtos('内集卡控制')


# @pytest.mark.skip
@allure.story('5.装船流程')
@allure.title('4.无结构船舶监控')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(),'05_PutBoxIntoShipProcess','loadship.yaml')))
def testship_monitor(driver, input):
    """无结构船舶监控"""
    menu = GtosMenu(driver)
    menu.select_level_Menu("船舶监控,无结构船舶监控")
    Monitor = NO_Structure_Monitoring(driver)
    Monitor.Retrieve()
    Monitor.clickLadeShipTag()
    Monitor.LadeShip_check_values(input,config.outBoxNumber)
    Monitor.LadeShip_Send_Box()
    Tag(driver).closeTagGtos('无结构船舶监控')

# @pytest.mark.skip
@allure.story('5.装船流程')
@allure.title('5.作业指令监控')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(),'05_PutBoxIntoShipProcess','loadship.yaml')))
def testship_order(driver, input):
    """作业指令监控"""
    menu = GtosMenu(driver)
    menu.select_level_Menu("机械控制,作业指令监控")
    work = Job_Order_Monitoring(driver)
    work.Retrieve(input,config.outportNumber,config.outBoxNumber)
    work.order_info_check(input,config.outBoxNumber)
    work.charge_car(input)
    work.send_box(input)
    work.LadeShip_confirm(input)
    Tag(driver).closeTagGtos('作业指令监控')

if __name__ == '__main__':
    #pytest.main(['-vs'])
    pytest.main(['-s', '-v', 'test_EnterBoxProcess.py','--html=../report/report.html', '--alluredir','../report/allure-results'])