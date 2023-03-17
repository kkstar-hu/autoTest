import os
import allure
import pytest
from Commons.Controls.tag import Tag
from GTOS.Config import config
from GTOS.PageObject.Control_Ship.Structure_Monitoring import Structure_Monitoring
from GTOS.PageObject.Mechanical_Control.Inset_Car import Inset_Car
from GTOS.PageObject.gtos_menu import GtosMenu
from Commons.yamlread import read_yaml
from GTOS.PageObject.DataManagement.ImportInformation_manifest import Manifest
from GTOS.PageObject.DataManagement.ImportDataVerification import Import_data_verification
from GTOS.PageObject.Mechanical_Control.Job_Order_Monitoring import Job_Order_Monitoring
import warnings
warnings.filterwarnings("ignore")


# @pytest.mark.skipif
# @pytest.mark.parametrize("input", read_yaml('discharging_process.yaml'))
@allure.story('2.大船卸船流程')
@allure.title('1、新增舱单')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(),'02_DischargingProcess', 'discharging_process.yaml')))
def testManifest(driver,input):
    """新增舱单资料"""
    menu = GtosMenu(driver)
    menu.select_level_Menu("资料管理,进口资料,舱单")
    manifest = Manifest(driver)
    manifest.AddManifest(input,config.boxNumber)

# @pytest.mark.skipif
# @pytest.mark.parametrize("input", read_yaml('discharging_process.yaml'))
@allure.story('2.大船卸船流程')
@allure.title('2、新增舱单箱')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(),'02_DischargingProcess', 'discharging_process.yaml')))
def testManifest_box(driver, input):
    """新增舱单箱资料"""
    manifest = Manifest(driver)
    manifest.AddBox(input,config.boxNumber)
    manifest.choice_ship()
    Tag(driver).closeTagGtos('舱单')

# @pytest.mark.skipif
@allure.story('2.大船卸船流程')
@allure.title('3、箱校验安排箱位置')
@pytest.mark.parametrize("input",read_yaml(os.path.join(os.getcwd(),'01_DataProcess','immediata_plan.yaml')))
def testSImport_data_verification(driver, input):
    """无结构靠泊、吊桥分配"""
    menu = GtosMenu(driver)
    menu.select_level_Menu("资料管理,进口资料,进口资料校验")
    idv = Import_data_verification(driver)
    idv.retrieval()
    idv.verification()
    Tag(driver).closeTagGtos('进口资料校验')

# @pytest.mark.skipif
@allure.story('2.大船卸船流程')
@allure.title('4、大船发箱')
@pytest.mark.parametrize("input",read_yaml(os.path.join(os.getcwd(),'01_DataProcess','immediata_plan.yaml')))
def testShip_sendbox(driver, input):
    """有结构发箱"""
    menu = GtosMenu(driver)
    menu.select_level_Menu("船舶监控,有结构船舶监控")
    nostructure = Structure_Monitoring(driver)
    nostructure.Retrieve(input)
    nostructure.LadeShip_Send_Box(config.boxNumber)
    Tag(driver).closeTagGtos('有结构船舶监控')

# @pytest.mark.skipif
# @pytest.mark.parametrize("input", read_yaml('discharging_process.yaml'))
@allure.story('2.卸船流程')
@allure.title('4、内集卡控制')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(),'02_DischargingProcess', 'discharging_process.yaml')))
def testCharge_Car(driver, input):
    """查看内集卡"""
    menu = GtosMenu(driver)
    menu.select_level_Menu("机械控制,内集卡控制")
    inset_car = Inset_Car(driver)
    inset_car.choice_job('A02')
    inset_car.choice_cars('作业步骤','空车')
    Tag(driver).closeTagGtos('内集卡控制')

# @pytest.mark.skipif
# @pytest.mark.parametrize("input", read_yaml('discharging_process.yaml'))
@allure.story('2.卸船流程')
@allure.title('5、工作指令操作')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(),'02_DischargingProcess', 'discharging_process.yaml')))
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


if __name__ == '__main__':
    pytest.main(['-sv'])