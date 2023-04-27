import os
import allure
import pytest
from Commons.Controls.tag import Tag
from GTOSXM.Config import config
from GTOSXM.PageObject.Control_Ship.Structure_Monitoring import Structure_Monitoring
from GTOSXM.PageObject.Mechanical_Control.Inset_Car import Inset_Car
from GTOSXM.PageObject.gtos_menu import GtosMenu
from Commons.yamlread import read_yaml
from GTOSXM.PageObject.DataManagement.ImportInformation_manifest import Manifest
from GTOSXM.PageObject.DataManagement.ImportDataVerification import Import_data_verification
from GTOSXM.PageObject.Mechanical_Control.Job_Order_Monitoring import Job_Order_Monitoring
import warnings

warnings.filterwarnings("ignore")


@allure.story('2.大船卸船流程')
@allure.title('1、新增舱单')
@pytest.mark.parametrize("input",read_yaml(os.path.join(os.getcwd(), '02_DischargingProcess', 'discharging_process.yaml')))
def testManifest(driver, input):
    """新增舱单资料"""
    menu = GtosMenu(driver)
    menu.select_level_Menu("资料管理,进口资料,舱单")
    manifest = Manifest(driver)
    manifest.AddManifest(input, config.boxNumber)
    manifest.AddBox(input, config.boxNumber)
    manifest.choice_ship()
    Tag(driver).closeTagGtos('舱单')


# @pytest.mark.skipif
@allure.story('2.大船卸船流程')
@allure.title('2、箱校验安排箱位置')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(), '01_DataProcess', 'immediata_plan.yaml')))
def testSImport_data_verification(driver, input):
    """资料校验"""
    menu = GtosMenu(driver)
    menu.select_level_Menu("资料管理,进口资料,进口资料校验")
    idv = Import_data_verification(driver)
    idv.retrieval()
    idv.verification('010582')
    Tag(driver).closeTagGtos('进口资料校验')


# @pytest.mark.skipif
@allure.story('2.大船卸船流程')
@allure.title('3、大船发箱')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(), '01_DataProcess', 'immediata_plan.yaml')))
def testShip_sendbox(driver, input):
    """有结构发箱"""
    menu = GtosMenu(driver)
    menu.select_level_Menu("船舶监控,有结构船舶监控")
    nostructure = Structure_Monitoring(driver)
    nostructure.Retrieve(input, config.importNumber)
    nostructure.mouse_job()
    # 切换窗口
    cls = driver.window_handles
    driver.switch_to.window(cls[1])
    nostructure.new_windows_choicebox(config.boxNumber)     # 箱查找
    nostructure.new_windows_job()    # 作业顺序
    nostructure.new_windows_sendbox()      # 发箱
    nostructure.selective_bridge(config.boxNumber)
    driver.close()
    # 切回原来窗口
    driver.switch_to.window((cls[0]))
    Tag(driver).closeTagGtos('有结构船舶监控')


# @pytest.mark.skipif
# @pytest.mark.parametrize("input", read_yaml('discharging_process.yaml'))
@allure.story('2.大船卸船流程')
@allure.title('4、内集卡控制')
@pytest.mark.parametrize("input",
                         read_yaml(os.path.join(os.getcwd(), '02_DischargingProcess', 'discharging_process.yaml')))
def testCharge_Car(driver, input):
    """查看内集卡"""
    menu = GtosMenu(driver)
    menu.select_level_Menu("机械控制,内集卡控制")
    inset_car = Inset_Car(driver)
    inset_car.choice_job('ALL')
    inset_car.choice_cars('作业步骤', '等待装车')
    Tag(driver).closeTagGtos('内集卡控制')


# @pytest.mark.skipif
# @pytest.mark.parametrize("input", read_yaml('discharging_process.yaml'))
@allure.story('2.大船卸船流程')
@allure.title('5、工作指令操作')
@pytest.mark.parametrize("input",
                         read_yaml(os.path.join(os.getcwd(), '02_DischargingProcess', 'discharging_process.yaml')))
def testJob(driver, input):
    """工作指令--改配集卡"""
    menu = GtosMenu(driver)
    menu.select_level_Menu("机械控制,作业指令监控")
    charge_car = Job_Order_Monitoring(driver)
    charge_car.Retrieve(input, config.importNumber, config.boxNumber)
    charge_car.order_info_check_new(input, config.boxNumber)
    charge_car.charge_car(input)
    charge_car.discharging_confirm(input)
    charge_car.closed_box(input)
    Tag(driver).closeTagGtos('作业指令监控')

