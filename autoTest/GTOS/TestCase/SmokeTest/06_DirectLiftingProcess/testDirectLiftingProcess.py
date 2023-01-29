import os
import allure
import pytest
from Commons.Controls.tag import Tag
from GTOS.Config import config
from GTOS.PageObject.Control_Ship.No_Structure_Monitoring import NO_Structure_Monitoring
from GTOS.PageObject.CrossingManagement.StraightLoad_StraightLif_tManagement import StraightLoad_StraightLift_Management
from GTOS.PageObject.DataManagement.ImportInformation_manifest import Manifest
from GTOS.PageObject.Mechanical_Control.Job_Order_Monitoring import Job_Order_Monitoring
from GTOS.PageObject.gtos_menu import GtosMenu
from Commons.yamlread import read_yaml
from GTOS.PageObject.Acceptance_Plan.Pick_up_Acceptance import Packing_up
from GTOS.PageObject.CrossingManagement.carOut import Car_Out

# @pytest.mark.skipif
# @pytest.mark.parametrize("input", read_yaml('direct_liftin_process.yaml'))
@allure.title('1、新增舱单计划')
@allure.story('7.直提流程')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(),'06_DirectLiftingProcess', 'direct_liftin_process.yaml')))
def testManifest(driver,input):
    """新增舱单资料"""
    menu = GtosMenu(driver)
    menu.select_level_Menu("资料管理,进口资料,舱单")
    manifest = Manifest(driver)
    manifest.AddManifest(input,config.boxNumberTwo)

# @pytest.mark.skipif
# @pytest.mark.parametrize("input", read_yaml('direct_liftin_process.yaml'))
@allure.title('2、新增提箱计划')
@allure.story('7.直提流程')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(),'06_DirectLiftingProcess', 'direct_liftin_process.yaml')))
def testManifest_box(driver, input):
    """新增舱单箱资料"""
    manifest = Manifest(driver)
    manifest.AddBox(input,config.boxNumberTwo)
    manifest.choice_ship()
    Tag(driver).closeTagGtos('舱单')


# @pytest.mark.skipif
# @pytest.mark.parametrize("input", read_yaml('direct_liftin_process.yaml'))
@allure.title('3、生成直提计划')
@allure.story('7.直提流程')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(),'06_DirectLiftingProcess', 'direct_liftin_process.yaml')))
def testPacking(driver,input):
    """提箱受理"""
    menu = GtosMenu(driver)
    menu.select_level_Menu("计划受理,安排计划,提箱受理")
    packing = Packing_up(driver)
    packing.straight_process(input,config.boxNumberTwo)
    Tag(driver).closeTagGtos('提箱受理')

# @pytest.mark.skipif
# @pytest.mark.parametrize("input", read_yaml('direct_liftin_process.yaml'))
@allure.title('4、直提报到')
@allure.story('7.直提流程')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(),'06_DirectLiftingProcess', 'direct_liftin_process.yaml')))
def testDirectLoading(driver,input):
    """直提"""
    menu = GtosMenu(driver)
    menu.select_level_Menu("道口管理,直装/直提管理")
    loading = StraightLoad_StraightLift_Management(driver)
    loading.process_lifting(input,config.boxNumberTwo)
    Tag(driver).closeTagGtos('直装/直提管理')

# @pytest.mark.skipif
# @pytest.mark.parametrize("input", read_yaml('direct_liftin_process.yaml'))
@allure.title('5、无结构船舶监控允许直提')
@allure.story('7.直提流程')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(),'06_DirectLiftingProcess', 'direct_liftin_process.yaml')))
def testLifting(driver, input):
    """无结构船舶允许直提"""
    menu = GtosMenu(driver)
    menu.select_level_Menu("船舶监控,无结构船舶监控")
    send_box = NO_Structure_Monitoring(driver)
    send_box.choice_lifting(input,config.boxNumberTwo)
    Tag(driver).closeTagGtos('无结构船舶监控')

# @pytest.mark.skipif
# @pytest.mark.parametrize("input", read_yaml('direct_liftin_process.yaml'))
@allure.title('6、工作指令卸船确认')
@allure.story('7.直提流程')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(),'06_DirectLiftingProcess', 'direct_liftin_process.yaml')))
def testOrder(driver, input):
    """工作指令-卸船确认"""
    menu = GtosMenu(driver)
    menu.select_level_Menu("机械控制,作业指令监控")
    charge_car = Job_Order_Monitoring(driver)
    charge_car.lifting_Order(input,config.importNumber,config.boxNumberTwo)
    Tag(driver).closeTagGtos('作业指令监控')


# @pytest.mark.skipif
# @pytest.mark.parametrize("input", read_yaml('direct_liftin_process.yaml'))
@allure.title('7、车辆出场')
@allure.story('7.直提流程')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(),'06_DirectLiftingProcess', 'direct_liftin_process.yaml')))
def testCar_Out(driver, input):
    """车辆出场"""
    menu = GtosMenu(driver)
    menu.select_level_Menu("道口管理,车辆出场")
    car_out = Car_Out(driver)
    car_out.process_loading(input,config.boxNumberTwo)
    Tag(driver).closeTagGtos('车辆出场')



if __name__ == '__main__':
    pytest.main(['-sv'])