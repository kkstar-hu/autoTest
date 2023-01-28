import os
import allure
import pytest
from Commons.Controls.tag import Tag
from GTOS.Config import config
from GTOS.PageObject.gtos_menu import GtosMenu
from Commons.yamlread import read_yaml
from GTOS.PageObject.DataManagement.ImportInformation_manifest import Manifest
from GTOS.PageObject.Control_Ship.No_Structure_Monitoring import NO_Structure_Monitoring
from GTOS.PageObject.Mechanical_Control.Job_Order_Monitoring import Job_Order_Monitoring


# @pytest.mark.skipif
# @pytest.mark.parametrize("input", read_yaml('discharging_process.yaml'))
@allure.title('1、新增舱单')
@allure.story('2.卸船流程')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(),'02_DischargingProcess', 'discharging_process.yaml')))
def testManifest(driver,input):
    """新增舱单资料"""
    menu = GtosMenu(driver)
    menu.select_level_Menu("资料管理,进口资料,舱单")
    manifest = Manifest(driver)
    manifest.AddManifest(input,config.boxNumber)

# @pytest.mark.skipif
# @pytest.mark.parametrize("input", read_yaml('discharging_process.yaml'))
@allure.title('2、新增舱单箱')
@allure.story('2.卸船流程')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(),'02_DischargingProcess', 'discharging_process.yaml')))
def testManifest_box(driver, input):
    """新增舱单箱资料"""
    manifest = Manifest(driver)
    manifest.AddBox(input,config.boxNumber)
    manifest.choice_ship()
    Tag(driver).closeChoiceTag('舱单')

# @pytest.mark.skipif
# @pytest.mark.parametrize("input", read_yaml('discharging_process.yaml'))
@allure.title('3、无结构监控发箱')
@allure.story('2.卸船流程')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(),'02_DischargingProcess', 'discharging_process.yaml')))
def testSend_box(driver, input):
    """无结构船舶发箱"""
    menu = GtosMenu(driver)
    menu.select_level_Menu("船舶监控,无结构船舶监控")
    send_box = NO_Structure_Monitoring(driver)
    send_box.Send_Box(input,config.boxNumber)
    Tag(driver).closeChoiceTag('无结构船舶监控')

# @pytest.mark.skipif
# @pytest.mark.parametrize("input", read_yaml('discharging_process.yaml'))
@allure.title('4、工作指令操作')
@allure.story('2.卸船流程')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(),'02_DischargingProcess', 'discharging_process.yaml')))
def testCharge_Car(driver, input):
    """工作指令--改配集卡"""
    menu = GtosMenu(driver)
    menu.select_level_Menu("机械控制,作业指令监控")
    charge_car = Job_Order_Monitoring(driver)
    charge_car.Job_DischargingOrder(input,config.importNumber,config.boxNumber)
    Tag(driver).closeChoiceTag('作业指令监控')


if __name__ == '__main__':
    pytest.main(['-sv'])