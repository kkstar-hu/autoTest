import os
import allure
import pytest
from Commons.Controls.tag import Tag
from GTOSXM.Config import config
from GTOSXM.PageObject.gtos_menu import GtosMenu
from Commons.yamlread import read_yaml
from GTOSXM.PageObject.DataManagement.ImportInformation_manifest import Manifest
from GTOSXM.PageObject.Control_Ship.No_Structure_Monitoring import NO_Structure_Monitoring
from GTOSXM.PageObject.Mechanical_Control.Job_Order_Monitoring import Job_Order_Monitoring
from GTOSXM.PageObject.Mechanical_Control.Inset_Car import Inset_Car


# @pytest.mark.skipif
@allure.story('2.卸船流程')
@allure.title('1、新增舱单')
@pytest.mark.parametrize("input",
                         read_yaml(os.path.join(os.getcwd(), '02_DischargingProcess', 'discharging_process.yaml')))
def testManifest(driver, input):
    """新增舱单资料"""
    menu = GtosMenu(driver)
    menu.select_level_Menu("资料管理,进口资料,舱单")
    manifest = Manifest(driver)
    manifest.AddManifest(input, config.boxNumber)


# @pytest.mark.skipif
@allure.story('2.卸船流程')
@allure.title('2、新增舱单箱')
@pytest.mark.parametrize("input",
                         read_yaml(os.path.join(os.getcwd(), '02_DischargingProcess', 'discharging_process.yaml')))
def testManifest_box(driver, input):
    """新增舱单箱资料"""
    manifest = Manifest(driver)
    manifest.AddBox(input, config.boxNumber)
    manifest.choice_ship()
    Tag(driver).closeTagGtos('舱单')


# @pytest.mark.skipif
@allure.story('2.卸船流程')
@allure.title('3、无结构监控发箱')
@pytest.mark.parametrize("input",
                         read_yaml(os.path.join(os.getcwd(), '02_DischargingProcess', 'discharging_process.yaml')))
def testSend_box(driver, input):
    """无结构船舶发箱"""
    menu = GtosMenu(driver)
    menu.select_level_Menu("船舶监控,无结构船舶监控")
    send_box = NO_Structure_Monitoring(driver)
    send_box.Retrieve()
    send_box.SendBox_check_values(input, config.boxNumber)
    send_box.Send_Box(config.boxNumber)
    Tag(driver).closeTagGtos('无结构船舶监控')


# @pytest.mark.skipif
@allure.story('2.卸船流程')
@allure.title('4、内集卡控制')
@pytest.mark.parametrize("input",
                         read_yaml(os.path.join(os.getcwd(), '02_DischargingProcess', 'discharging_process.yaml')))
def testCharge_Car(driver, input):
    """查看内集卡"""
    menu = GtosMenu(driver)
    menu.select_level_Menu("机械控制,内集卡控制")
    inset_car = Inset_Car(driver)
    inset_car.choice_job('ALL')
    inset_car.choice_cars('作业步骤', '空车')
    Tag(driver).closeTagGtos('内集卡控制')


# @pytest.mark.skipif
@allure.story('2.卸船流程')
@allure.title('5、工作指令操作')
@pytest.mark.parametrize("input",
                         read_yaml(os.path.join(os.getcwd(), '02_DischargingProcess', 'discharging_process.yaml')))
def testJob(driver, input):
    """工作指令"""
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
