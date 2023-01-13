import os
import allure
import pytest
from Commons.Controls.tag import Tag
from GTOS.PageObject.Control_Ship.No_Structure_Monitoring import NO_Structure_Monitoring
from GTOS.PageObject.CrossingManagement.carOut import Car_Out
from GTOS.PageObject.Mechanical_Control.Job_Order_Monitoring import Job_Order_Monitoring
from GTOS.PageObject.gtos_menu import GtosMenu
from Commons.yamlread import read_yaml
from GTOS.PageObject.Acceptance_Plan.InBoxAcceptance import InBox_Acceptance
from GTOS.PageObject.DataManagement.ExitInformation_manifest import Manifest
from GTOS.PageObject.Ship_Planning.No_Structure_Stowage import No_Structure_Stowage
from GTOS.PageObject.CrossingManagement.StraightLoad_StraightLif_tManagement import StraightLoad_StraightLift_Management

# @pytest.mark.skipif
# @pytest.mark.parametrize("input", read_yaml('direct_loadingp_rocess.yaml'))
@allure.title('1、新建进场直装计划')
@allure.story('6.直装流程')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(),'07_DirectLoadingProcess', 'direct_loadingp_rocess.yaml')))
def testAddPlan(driver,input):
    """新增进场直装计划"""
    menu = GtosMenu(driver)
    menu.select_level_Menu("计划受理,安排计划,进箱受理")
    inbox = InBox_Acceptance(driver)
    inbox.process(input)
    Tag(driver).closeChoiceTag('进箱受理')

# @pytest.mark.skipif
# @pytest.mark.parametrize("input", read_yaml('direct_loadingp_rocess.yaml'))
@allure.title('2、码头人放行')
@allure.story('6.直装流程')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(),'07_DirectLoadingProcess', 'direct_loadingp_rocess.yaml')))
def testWharfrelease(driver,input):
    """码头人放行"""
    menu = GtosMenu(driver)
    menu.select_level_Menu("资料管理,出口资料,装船箱放行")
    release = Manifest(driver)
    release.input_values(input)
    Tag(driver).closeChoiceTag('装船箱放行')

# @pytest.mark.skipif
# @pytest.mark.parametrize("input", read_yaml('direct_loadingp_rocess.yaml'))
@allure.title('3、无结构船舶配载')
@allure.story('6.直装流程')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(),'07_DirectLoadingProcess', 'direct_loadingp_rocess.yaml')))
def testNoStowage(driver,input):
    """无结构船舶配载"""
    menu = GtosMenu(driver)
    menu.select_level_Menu("船舶策划,无结构船舶配载")
    no_ship = No_Structure_Stowage(driver)
    no_ship.Retrieve(input)
    Tag(driver).closeChoiceTag('无结构船舶配载')

# @pytest.mark.skipif
# @pytest.mark.parametrize("input", read_yaml('direct_loadingp_rocess.yaml'))
@allure.title('4、直装/直提管理')
@allure.story('6.直装流程')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(),'07_DirectLoadingProcess', 'direct_loadingp_rocess.yaml')))
def testDirectLoading(driver,input):
    """直装/直提"""
    menu = GtosMenu(driver)
    menu.select_level_Menu("道口管理,直装/直提管理")
    loading = StraightLoad_StraightLift_Management(driver)
    loading.process_loading(input)
    Tag(driver).closeChoiceTag('直装/直提管理')

# @pytest.mark.skipif
@allure.title('5、无结构监控允许直装')
@allure.story('6.直装流程')
# @pytest.mark.parametrize("input", read_yaml('direct_loadingp_rocess.yaml'))
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(),'07_DirectLoadingProcess', 'direct_loadingp_rocess.yaml')))
def testSend_box(driver, input):
    """无结构船舶发箱"""
    menu = GtosMenu(driver)
    menu.select_level_Menu("船舶监控,无结构船舶监控")
    send_box = NO_Structure_Monitoring(driver)
    send_box.choice_loading(input)
    Tag(driver).closeChoiceTag('无结构船舶监控')

@allure.title('6、工作指令操作')
@allure.story('6.直装流程')
# @pytest.mark.parametrize("input", read_yaml('direct_loadingp_rocess.yaml'))
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(),'07_DirectLoadingProcess', 'direct_loadingp_rocess.yaml')))
def testOrder(driver, input):
    """工作指令--装船确认"""
    menu = GtosMenu(driver)
    menu.select_level_Menu("机械控制,作业指令监控")
    charge_car = Job_Order_Monitoring(driver)
    charge_car.loading_PackingboxOrder(input)
    Tag(driver).closeChoiceTag('作业指令监控')

@allure.title('7、车辆出场')
@allure.story('6.直装流程')
# @pytest.mark.parametrize("input", read_yaml('direct_loadingp_rocess.yaml'))
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(),'07_DirectLoadingProcess', 'direct_loadingp_rocess.yaml')))
def testCar_Out(driver, input):
    """车辆出场"""
    menu = GtosMenu(driver)
    menu.select_level_Menu("道口管理,车辆出场")
    car_out = Car_Out(driver)
    car_out.process_loading(input)
    Tag(driver).closeChoiceTag('车辆出场')


if __name__ == '__main__':
    pytest.main(['-sv'])