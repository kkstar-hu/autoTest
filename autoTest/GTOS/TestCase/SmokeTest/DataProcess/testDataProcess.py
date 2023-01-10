import os
import allure
import pytest
from Commons.Controls.tag import Tag
from GTOS.PageObject.gtos_menu import GtosMenu
from GTOS.PageObject.Barge_Planning.Immediate_Plan import Immediate_plan
from GTOS.PageObject.Barge_Planning.Bridge_Crane_distribution import Bridge_Crane_Distribution
from GTOS.PageObject.Barge_Planning.Voyage_Attached import Voyage_Attached
from GTOS.PageObject.Yard_Planning.Stockpiling_Planning import Stockpiling_Planning
from GTOS.PageObject.Control_Ship.No_Structure_Monitoring import NO_Structure_Monitoring
from Commons.yamlread import read_yaml

# @pytest.mark.skipif
@pytest.mark.parametrize("input", read_yaml('immediata_plan.yaml'))
@allure.title('1、近期计划')
@allure.story('0.数据准备')
# @pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(),'DirectLiftingProcess', 'direct_liftin_process.yaml')))
def testImmediatePlan(driver,input):
    """近期计划"""
    menu = GtosMenu(driver)
    menu.select_level_Menu("泊位策划,近期计划")
    plan = Immediate_plan(driver)
    plan.Immediate_plan_process(input)
    Tag(driver).closeChoiceTag('近期计划')

# @pytest.mark.skipif
@pytest.mark.parametrize("input", read_yaml('immediata_plan.yaml'))
@allure.title('2、桥吊资源分配')
@allure.story('0.数据准备')
# @pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(),'DirectLiftingProcess', 'direct_liftin_process.yaml')))
def testBridgeCraneDistribution(driver,input):
    """桥吊资源分配"""
    menu = GtosMenu(driver)
    menu.select_level_Menu("泊位策划,桥吊资源分配")
    bridge = Bridge_Crane_Distribution(driver)
    bridge.process(input)
    Tag(driver).closeChoiceTag('桥吊资源分配')

# @pytest.mark.skipif
@pytest.mark.parametrize("input", read_yaml('immediata_plan.yaml'))
@allure.title('3、航次挂靠港')
@allure.story('0.数据准备')
# @pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(),'DirectLiftingProcess', 'direct_liftin_process.yaml')))
def testVoyage_Attached(driver,input):
    """航次挂靠港"""
    menu = GtosMenu(driver)
    menu.select_level_Menu("泊位策划,航次挂靠港")
    vovage = Voyage_Attached(driver)
    vovage.process(input)
    Tag(driver).closeChoiceTag('航次挂靠港')

# @pytest.mark.skipif
@pytest.mark.parametrize("input", read_yaml('immediata_plan.yaml'))
@allure.title('4、堆存计划-道口进')
@allure.story('0.数据准备')
# @pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(),'DirectLiftingProcess', 'direct_liftin_process.yaml')))
def testStockpiling_Planning_into(driver,input):
    """堆存计划-道口进"""
    menu = GtosMenu(driver)
    menu.select_level_Menu("堆场策划,堆存,堆存计划")
    stockpiling = Stockpiling_Planning(driver)
    stockpiling.process_into(input)

# @pytest.mark.skipif
@pytest.mark.parametrize("input", read_yaml('immediata_plan.yaml'))
@allure.title('5、堆存计划-卸船')
@allure.story('0.数据准备')
# @pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(),'DirectLiftingProcess', 'direct_liftin_process.yaml')))
def testStockpiling_Planning_out(driver, input):
    """堆存计划-卸船"""
    stockpiling = Stockpiling_Planning(driver)
    stockpiling.process_out(input)
    Tag(driver).closeChoiceTag('堆存计划')

# @pytest.mark.skipif
@pytest.mark.parametrize("input", read_yaml('immediata_plan.yaml'))
@allure.title('5、堆存计划-卸船')
@allure.story('0.数据准备')
# @pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(),'DirectLiftingProcess', 'direct_liftin_process.yaml')))
def testShip_operation(driver, input):
    """无结构靠泊、吊桥分配"""
    menu = GtosMenu(driver)
    menu.select_level_Menu("船舶监控,无结构船舶监控")
    nostructure = NO_Structure_Monitoring(driver)
    nostructure.ship_operation(input)
    Tag(driver).closeChoiceTag('无结构船舶监控')

if __name__ == '__main__':
    pytest.main(['-sv'])