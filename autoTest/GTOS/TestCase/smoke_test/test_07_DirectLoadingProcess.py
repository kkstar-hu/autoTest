import os
import allure
import pytest
from Commons.Controls.tag import Tag
from GTOS.Config import config
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
@allure.story('7.直装流程')
@allure.title('1、新建进场直装计划')
@pytest.mark.parametrize("input",
                         read_yaml(os.path.join(os.getcwd(), '07_DirectLoadingProcess', 'direct_loadingp_rocess.yaml')))
def testAddPlan(driver, input):
    """新增进场直装计划"""
    menu = GtosMenu(driver)
    menu.select_level_Menu("计划受理,安排计划,进箱受理")
    inbox = InBox_Acceptance(driver)
    inbox.choice_tree_straight(input)
    inbox.select_value()
    inbox.addPlan(input, config.boxNumberThree)
    inbox.Add_value(config.boxNumberThree)
    inbox.build_plan(input)
    Tag(driver).closeTagGtos('进箱受理')


# @pytest.mark.skipif
# @pytest.mark.parametrize("input", read_yaml('direct_loadingp_rocess.yaml'))
@allure.story('7.直装流程')
@allure.title('2、码头人放行')
@pytest.mark.parametrize("input",
                         read_yaml(os.path.join(os.getcwd(), '07_DirectLoadingProcess', 'direct_loadingp_rocess.yaml')))
def testWharfrelease(driver, input):
    """码头人放行"""
    menu = GtosMenu(driver)
    menu.select_level_Menu("资料管理,出口资料,装船箱放行")
    release = Manifest(driver)
    release.input_values(input, config.boxNumberThree)
    Tag(driver).closeTagGtos('装船箱放行')


# @pytest.mark.skipif
# @pytest.mark.parametrize("input", read_yaml('direct_loadingp_rocess.yaml'))
@allure.story('7.直装流程')
@allure.title('3、无结构船舶配载')
@pytest.mark.parametrize("input",
                         read_yaml(os.path.join(os.getcwd(), '07_DirectLoadingProcess', 'direct_loadingp_rocess.yaml')))
def testNoStowage(driver, input):
    """无结构船舶配载"""
    menu = GtosMenu(driver)
    menu.select_level_Menu("船舶策划,无结构船舶配载")
    stowage = No_Structure_Stowage(driver)
    stowage.search()
    stowage.check(input, config.boxNumberThree)
    stowage.stowage(config.boxNumberThree)
    Tag(driver).closeTagGtos('无结构船舶配载')


# @pytest.mark.skipif
# @pytest.mark.parametrize("input", read_yaml('direct_loadingp_rocess.yaml'))
@allure.story('7.直装流程')
@allure.title('4、直装/直提管理')
@pytest.mark.parametrize("input",
                         read_yaml(os.path.join(os.getcwd(), '07_DirectLoadingProcess', 'direct_loadingp_rocess.yaml')))
def testDirectLoading(driver, input):
    """直装/直提"""
    menu = GtosMenu(driver)
    menu.select_level_Menu("道口管理,直装/直提管理")
    loading = StraightLoad_StraightLift_Management(driver)
    loading.loading_value(input, config.boxNumberThree)
    loading.loading_report(input)
    Tag(driver).closeTagGtos('直装/直提管理')


# @pytest.mark.skipif
@allure.story('7.直装流程')
@allure.title('5、无结构监控允许直装')
# @pytest.mark.parametrize("input", read_yaml('direct_loadingp_rocess.yaml'))
@pytest.mark.parametrize("input",
                         read_yaml(os.path.join(os.getcwd(), '07_DirectLoadingProcess', 'direct_loadingp_rocess.yaml')))
def testSend_box(driver, input):
    """无结构船舶发箱"""
    menu = GtosMenu(driver)
    menu.select_level_Menu("船舶监控,无结构船舶监控")
    send_box = NO_Structure_Monitoring(driver)
    send_box.choice_loading(input, config.boxNumberThree)
    Tag(driver).closeTagGtos('无结构船舶监控')


# @pytest.mark.skipif
@allure.story('7.直装流程')
@allure.title('6、工作指令操作')
# @pytest.mark.parametrize("input", read_yaml('direct_loadingp_rocess.yaml'))
@pytest.mark.parametrize("input",
                         read_yaml(os.path.join(os.getcwd(), '07_DirectLoadingProcess', 'direct_loadingp_rocess.yaml')))
def testOrder(driver, input):
    """工作指令--装船确认"""
    menu = GtosMenu(driver)
    menu.select_level_Menu("机械控制,作业指令监控")
    charge_car = Job_Order_Monitoring(driver)
    charge_car.Retrieve(input, config.outportNumber, config.boxNumberThree)
    charge_car.order_info_check_new(input, config.boxNumberThree)
    charge_car.shipping_confirmation(input)
    Tag(driver).closeTagGtos('作业指令监控')


@allure.story('7.直装流程')
@allure.title('7、车辆出场')
@pytest.mark.parametrize("input",
                         read_yaml(os.path.join(os.getcwd(), '07_DirectLoadingProcess', 'direct_loadingp_rocess.yaml')))
def testCar_Out(driver, input):
    """车辆出场"""
    menu = GtosMenu(driver)
    menu.select_level_Menu("道口管理,车辆出场")
    car_out = Car_Out(driver)
    car_out.input_values(input, config.boxNumberThree)
    car_out.retrieve()
    car_out.confirm_out_loadingAndLifting()
    Tag(driver).closeTagGtos('车辆出场')


if __name__ == '__main__':
    pytest.main(['-sv'])
