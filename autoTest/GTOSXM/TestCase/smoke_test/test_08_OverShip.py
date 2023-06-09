import os
import allure
import pytest
from Commons.Controls.tag import Tag
from GTOSXM.Config import config
from GTOSXM.Controls.Gtos_table import Gtos_table
from GTOSXM.PageObject.DataManagement.closeFlight import CloseFlight
from GTOSXM.PageObject.gtos_menu import GtosMenu
from GTOSXM.PageObject.Barge_Planning.Immediate_Plan import Immediate_plan
from GTOSXM.PageObject.Control_Ship.No_Structure_Monitoring import NO_Structure_Monitoring
from Commons.yamlread import read_yaml


# @pytest.mark.skipif
@allure.title('1、吊桥完工')
@allure.story('8.离泊确认,航次关闭')
def testShip_operation(driver):
    """无结构靠泊、吊桥分配"""
    menu = GtosMenu(driver)
    menu.select_level_Menu("船舶监控,无结构船舶监控")
    nostructure = NO_Structure_Monitoring(driver)
    nostructure.Retrieve()
    nostructure.over_drawbridge("AUTO")
    nostructure.unberthing(config.importNumber)
    Tag(driver).closeTagGtos('无结构船舶监控')
    menu.select_level_Menu("资料管理,航次关闭")
    close = CloseFlight(driver)
    close.search(config.importNumber)
    close.closeFlight()
    Tag(driver).closeTagGtos('航次关闭')

@pytest.mark.skipif
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(), '01_DataProcess', 'immediata_plan.yaml')))
@allure.title('2、近期计划验证靠泊信息')
@allure.story('8.离泊确认,航次关闭')
def testCheck_shipinfo(driver, input):
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
