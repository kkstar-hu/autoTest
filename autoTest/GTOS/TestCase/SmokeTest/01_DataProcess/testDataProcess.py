import os
import allure
import pytest
from Commons.Controls.tag import Tag
from GTOS.Config import config
from GTOS.Controls.Gtos_table import Gtos_table
from GTOS.PageObject.gtos_menu import GtosMenu
from GTOS.PageObject.Barge_Planning.Immediate_Plan import Immediate_plan
from GTOS.PageObject.Barge_Planning.Bridge_Crane_distribution import Bridge_Crane_Distribution
from GTOS.PageObject.Barge_Planning.Voyage_Attached import Voyage_Attached
from GTOS.PageObject.Yard_Planning.Stockpiling_Planning import Stockpiling_Planning
from GTOS.PageObject.Control_Ship.No_Structure_Monitoring import NO_Structure_Monitoring
from Commons.yamlread import read_yaml



@allure.title('1、近期计划')
@allure.story('1.驳船流程功能准备')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(),'01_DataProcess', 'immediata_plan.yaml')))
def testImmediatePlan(driver,input):
    """近期计划"""
    menu = GtosMenu(driver)
    menu.select_level_Menu("泊位策划,近期计划")
    plan = Immediate_plan(driver)
    plan.switch_Barge()
    plan.Add_Plan(input)
    plan.checkPlan()
    plan.Sure_ShipPlan()
    plan.SureInBox()
    Tag(driver).closeChoiceTag('近期计划')


@pytest.mark.parametrize("input",read_yaml(os.path.join(os.getcwd(),'01_DataProcess','immediata_plan.yaml')))
@allure.title('2、桥吊资源分配')
@allure.story('1.驳船流程功能准备')
def testBridgeCraneDistribution(driver,input):
    """桥吊资源分配"""
    menu = GtosMenu(driver)
    menu.select_level_Menu("泊位策划,桥吊资源分配")
    bridge = Bridge_Crane_Distribution(driver)
    bridge.search(input)
    bridge.arrangeBridge()
    Tag(driver).closeChoiceTag('桥吊资源分配')


@pytest.mark.parametrize("input",read_yaml(os.path.join(os.getcwd(),'01_DataProcess','immediata_plan.yaml')))
@allure.title('3、航次挂靠港')
@allure.story('1.驳船流程功能准备')
def testVoyage_Attached(driver,input):
    """航次挂靠港"""
    menu = GtosMenu(driver)
    menu.select_level_Menu("泊位策划,航次挂靠港")
    vovage = Voyage_Attached(driver)
    vovage.process(input)
    Tag(driver).closeChoiceTag('航次挂靠港')

# @pytest.mark.skipif
@pytest.mark.parametrize("input",read_yaml(os.path.join(os.getcwd(),'01_DataProcess','immediata_plan.yaml')))
@allure.title('4、堆存计划-道口进')
@allure.story('1.驳船流程功能准备')
def testStockpiling_Planning_into(driver,input):
    """堆存计划-道口进"""
    menu = GtosMenu(driver)
    menu.select_level_Menu("堆场策划,堆存,堆存计划")
    stockpiling = Stockpiling_Planning(driver)
    stockpiling.process_into(input)

# @pytest.mark.skipif
@pytest.mark.parametrize("input",read_yaml(os.path.join(os.getcwd(),'01_DataProcess','immediata_plan.yaml')))
@allure.title('5、堆存计划-卸船')
@allure.story('1.驳船流程功能准备')
def testStockpiling_Planning_out(driver, input):
    """堆存计划-卸船"""
    stockpiling = Stockpiling_Planning(driver)
    stockpiling.process_out(input)
    Tag(driver).closeChoiceTag('堆存计划')

# @pytest.mark.skipif
@pytest.mark.parametrize("input",read_yaml(os.path.join(os.getcwd(),'01_DataProcess', 'immediata_plan.yaml')))
@allure.title('6、吊桥分配')
@allure.story('1.驳船流程功能准备')
def testShip_operation(driver, input):
    """无结构靠泊、吊桥分配"""
    menu = GtosMenu(driver)
    menu.select_level_Menu("船舶监控,无结构船舶监控")
    nostructure = NO_Structure_Monitoring(driver)
    nostructure.ship_operation(input)
    Tag(driver).closeChoiceTag('无结构船舶监控')

@pytest.mark.parametrize("input",read_yaml(os.path.join(os.getcwd(),'01_DataProcess', 'immediata_plan.yaml')))
@allure.title('7、近期计划验证靠泊信息')
@allure.story('1.驳船流程功能准备')
def testShip_operation(driver, input):
    """近期计划验证靠泊信息"""
    menu = GtosMenu(driver)
    menu.select_level_Menu("泊位策划,近期计划")
    plan = Immediate_plan(driver)
    plan.switch_Barge()
    tablecheck = Gtos_table(driver, 2)
    tablecheck.select_row("进口航次", config.importNumber)
    plan.check_alongside_info(input)

if __name__ == '__main__':
    pytest.main(['-sv'])