import os
import allure
import pytest
from Commons.Controls.tag import Tag
from GTOSXM.Config import config
from GTOSXM.PageObject.Control_Ship.No_Structure_Monitoring import NO_Structure_Monitoring
from GTOSXM.PageObject.CrossingManagement.StraightLoad_StraightLif_tManagement import StraightLoad_StraightLift_Management
from GTOSXM.PageObject.DataManagement.ImportInformation_manifest import Manifest
from GTOSXM.PageObject.Mechanical_Control.Job_Order_Monitoring import Job_Order_Monitoring
from GTOSXM.PageObject.gtos_menu import GtosMenu
from Commons.yamlread import read_yaml
from GTOSXM.PageObject.Acceptance_Plan.Pick_up_Acceptance import Packing_up
from GTOSXM.PageObject.CrossingManagement.carOut import Car_Out

# @pytest.mark.skipif
# @pytest.mark.parametrize("input", read_yaml('direct_liftin_process.yaml'))
@allure.story('6.直提流程')
@allure.title('1、新增舱单计划')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(),'06_DirectLiftingProcess', 'direct_liftin_process.yaml')))
def testManifest(driver,input):
    """新增舱单资料"""
    menu = GtosMenu(driver)
    menu.select_level_Menu("资料管理,进口资料,舱单")
    manifest = Manifest(driver)
    manifest.AddManifest(input,config.boxNumberTwo)

# @pytest.mark.skipif
# @pytest.mark.parametrize("input", read_yaml('direct_liftin_process.yaml'))
@allure.story('6.直提流程')
@allure.title('2、新增提箱计划')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(),'06_DirectLiftingProcess', 'direct_liftin_process.yaml')))
def testManifest_box(driver, input):
    """新增舱单箱资料"""
    manifest = Manifest(driver)
    manifest.AddBox(input,config.boxNumberTwo)
    manifest.choice_ship()
    Tag(driver).closeTagGtos('舱单')


# @pytest.mark.skipif
# @pytest.mark.parametrize("input", read_yaml('direct_liftin_process.yaml'))
@allure.story('6.直提流程')
@allure.title('3、生成直提计划')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(),'06_DirectLiftingProcess', 'direct_liftin_process.yaml')))
def testPacking(driver,input):
    """提箱受理"""
    menu = GtosMenu(driver)
    menu.select_level_Menu("计划受理,安排计划,提箱受理")
    packing = Packing_up(driver)
    packing.choice_tree(input)
    packing.select_value(config.boxNumberTwo)
    packing.retrieve(input, config.boxNumberTwo)
    packing.tick_off_box()
    packing.customs_release()
    packing.generation_plan()
    packing.save_over(input)
    Tag(driver).closeTagGtos('提箱受理')

# @pytest.mark.skipif
# @pytest.mark.parametrize("input", read_yaml('direct_liftin_process.yaml'))
@allure.story('6.直提流程')
@allure.title('4、直提报到')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(),'06_DirectLiftingProcess', 'direct_liftin_process.yaml')))
def testDirectLoading(driver,input):
    """直提"""
    menu = GtosMenu(driver)
    menu.select_level_Menu("道口管理,直装/直提管理")
    loading = StraightLoad_StraightLift_Management(driver)
    loading.switch_lift()
    loading.lifting_value(input, config.boxNumberTwo)
    loading.lifting_report(input)
    Tag(driver).closeTagGtos('直装/直提管理')

# @pytest.mark.skipif
# @pytest.mark.parametrize("input", read_yaml('direct_liftin_process.yaml'))
@allure.story('6.直提流程')
@allure.title('5、无结构船舶监控允许直提')
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
@allure.story('6.直提流程')
@allure.title('6、工作指令卸船确认')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(),'06_DirectLiftingProcess', 'direct_liftin_process.yaml')))
def testOrder(driver, input):
    """工作指令-卸船确认"""
    menu = GtosMenu(driver)
    menu.select_level_Menu("机械控制,作业指令监控")
    charge_car = Job_Order_Monitoring(driver)
    charge_car.Retrieve(input, config.importNumber, config.boxNumberTwo)
    charge_car.order_info_check_new(input, config.boxNumberTwo)
    charge_car.discharging_confirm_lifting(input)
    Tag(driver).closeTagGtos('作业指令监控')


# @pytest.mark.skipif
# @pytest.mark.parametrize("input", read_yaml('direct_liftin_process.yaml'))
@allure.title('7、车辆出场')
@allure.story('6.直提流程')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(),'06_DirectLiftingProcess', 'direct_liftin_process.yaml')))
def testCar_Out(driver, input):
    """车辆出场"""
    menu = GtosMenu(driver)
    menu.select_level_Menu("道口管理,车辆出场")
    car_out = Car_Out(driver)
    car_out.input_values(input, config.boxNumberTwo)
    car_out.retrieve()
    car_out.confirm_out_loadingAndLifting()
    Tag(driver).closeTagGtos('车辆出场')



if __name__ == '__main__':
    pytest.main(['-sv'])