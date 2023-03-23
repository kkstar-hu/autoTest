import os
import allure
import pytest
from Commons.Controls.tag import Tag
from GTOSXM.Config import config
from GTOSXM.Controls.Gtos_table import Gtos_table
from GTOSXM.PageObject.gtos_menu import GtosMenu
from GTOSXM.PageObject.Barge_Planning.Immediate_Plan import Immediate_plan
from GTOSXM.PageObject.Barge_Planning.Bridge_Crane_distribution import Bridge_Crane_Distribution
from GTOSXM.PageObject.Barge_Planning.Voyage_Attached import Voyage_Attached
from GTOSXM.PageObject.Yard_Planning.Stockpiling_Planning import Stockpiling_Planning
from GTOSXM.PageObject.Control_Ship.No_Structure_Monitoring import NO_Structure_Monitoring
from Commons.yamlread import read_yaml


# @pytest.mark.skipif
@allure.story('1.驳船流程功能准备')
@allure.title('1、近期计划')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(),'01_DataProcess', 'immediata_plan.yaml')))
def testImmediatePlan(driver,input):
    """近期计划"""
    print("******************************************Smoke Test Start***********************************************")
    menu = GtosMenu(driver)
    menu.select_level_Menu("泊位策划,近期计划")
    plan = Immediate_plan(driver)
    plan.switch_Barge()
    plan.Add_Plan(input)
    plan.checkPlan(2)
    plan.Sure_ShipPlan(2)
    plan.SureInBox()
    Tag(driver).closeTagGtos('近期计划')

# @pytest.mark.skipif
@allure.story('1.驳船流程功能准备')
@allure.title('2、桥吊资源分配')
@pytest.mark.parametrize("input",read_yaml(os.path.join(os.getcwd(),'01_DataProcess','immediata_plan.yaml')))
def testBridgeCraneDistribution(driver,input):
    """桥吊资源分配"""
    menu = GtosMenu(driver)
    menu.select_level_Menu("泊位策划,桥吊资源分配")
    bridge = Bridge_Crane_Distribution(driver)
    bridge.search(input)
    bridge.arrangeBridge()
    Tag(driver).closeTagGtos('桥吊资源分配')

# @pytest.mark.skipif


@allure.story('1.驳船流程功能准备')
@allure.title('3、航次挂靠港')
@pytest.mark.parametrize("input",read_yaml(os.path.join(os.getcwd(),'01_DataProcess','immediata_plan.yaml')))
def testVoyage_Attached(driver,input):
    """航次挂靠港"""
    menu = GtosMenu(driver)
    menu.select_level_Menu("泊位策划,航次挂靠港")
    vovage = Voyage_Attached(driver)
    vovage.input_values()
    vovage.Retrieval()
    vovage.close_alert('未找到相关航次挂靠港数据')
    vovage.Add()
    Tag(driver).closeTagGtos('航次挂靠港')

# @pytest.mark.skipif


@allure.story('1.驳船流程功能准备')
@allure.title('4、堆存计划-道口进')
@pytest.mark.parametrize("input",read_yaml(os.path.join(os.getcwd(),'01_DataProcess','immediata_plan.yaml')))
def testStockpiling_Planning_into(driver,input):
    """堆存计划-道口进"""
    menu = GtosMenu(driver)
    menu.select_level_Menu("堆场策划,堆存,堆存计划")
    stockpiling = Stockpiling_Planning(driver)
    stockpiling.search("道口进", config.outportNumber)
    stockpiling.close_alert('未找到相关堆存计划')
    stockpiling.Add_into_plan()
    stockpiling.Add_box_INTO()

# @pytest.mark.skipif


@allure.story('1.驳船流程功能准备')
@allure.title('5、堆存计划-卸船')
@pytest.mark.parametrize("input",read_yaml(os.path.join(os.getcwd(),'01_DataProcess','immediata_plan.yaml')))
def testStockpiling_Planning_out(driver, input):
    """堆存计划-卸船"""
    stockpiling = Stockpiling_Planning(driver)
    stockpiling.search("卸船", config.importNumber)
    stockpiling.Add_into_plan()
    stockpiling.Add_box_OUT()
    Tag(driver).closeTagGtos('堆存计划')

# @pytest.mark.skipif


@allure.story('1.驳船流程功能准备')
@allure.title('6、吊桥分配')
@pytest.mark.parametrize("input",read_yaml(os.path.join(os.getcwd(),'01_DataProcess', 'immediata_plan.yaml')))
def testShip_operation(driver, input):
    """无结构靠泊、吊桥分配"""
    menu = GtosMenu(driver)
    menu.select_level_Menu("船舶监控,无结构船舶监控")
    nostructure = NO_Structure_Monitoring(driver)
    nostructure.ship_operation(input)
    Tag(driver).closeTagGtos('无结构船舶监控')


if __name__ == '__main__':
    pytest.main(['-sv'])