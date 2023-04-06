import os
import allure
import pytest
from Commons.Controls.tag import Tag
from GTOSXM.Config import config
from GTOSXM.Controls.Gtos_table import Gtos_table
from GTOSXM.PageObject.DataManagement.closeFlight import CloseFlight
from GTOSXM.PageObject.gtos_menu import GtosMenu
from GTOSXM.PageObject.Barge_Planning.Immediate_Plan import Immediate_plan
from Commons.yamlread import read_yaml
from GTOSXM.PageObject.Control_Ship.Structure_Monitoring import Structure_Monitoring


# @pytest.mark.skipif
@allure.story('8.离泊确认,航次关闭')
@allure.title('6、靠泊确认和吊桥分配')
@pytest.mark.parametrize("input",read_yaml(os.path.join(os.getcwd(),'01_DataProcess','immediata_plan.yaml')))
def testShip_operation(driver, input):
    """有结构离泊离港、吊桥完工"""
    menu = GtosMenu(driver)
    menu.select_level_Menu("船舶监控,有结构船舶监控")
    nostructure = Structure_Monitoring(driver)
    nostructure.Retrieve(input,config.importNumber)
    nostructure.close_bridge()
    nostructure.leave_port()
    Tag(driver).closeTagGtos('有结构船舶监控')
    menu.select_level_Menu("资料管理,航次关闭")
    close=CloseFlight(driver)
    close.search(config.importNumber)
    close.closeFlight()
    Tag(driver).closeTagGtos('航次关闭')


@pytest.mark.skipif
@allure.story('8.离泊确认,航次关闭')
@allure.title('2、近期计划验证靠泊信息')
@pytest.mark.parametrize("input",read_yaml(os.path.join(os.getcwd(),'01_DataProcess', 'immediata_plan.yaml')))
def testCheck_shipinfo(driver, input):
    """近期计划验证靠泊信息"""
    menu = GtosMenu(driver)
    menu.select_level_Menu("泊位策划,近期计划")
    plan = Immediate_plan(driver)
    plan.checkPlan_over(1)

if __name__ == '__main__':
    pytest.main(['-sv'])