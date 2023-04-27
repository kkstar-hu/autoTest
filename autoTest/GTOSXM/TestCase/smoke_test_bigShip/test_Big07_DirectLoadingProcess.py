import json
import os
import allure
import pytest
from Base.baseinterface import RequestHandler
from Commons.Controls.tag import Tag
from Commons.jsonread import read_json
from GTOSXM.Config import config, configinterface
from GTOSXM.PageObject.Control_Ship.Structure_Monitoring import Structure_Monitoring
from GTOSXM.PageObject.CrossingManagement.carOut import Car_Out
from GTOSXM.PageObject.Mechanical_Control.Job_Order_Monitoring import Job_Order_Monitoring
from GTOSXM.PageObject.Ship_Planning.Structure_Stowage import Structure_Stowage
from GTOSXM.PageObject.gtos_menu import GtosMenu
from Commons.yamlread import read_yaml
from GTOSXM.PageObject.Acceptance_Plan.InBoxAcceptance import InBox_Acceptance
from GTOSXM.PageObject.DataManagement.ExitInformation_manifest import Manifest
from GTOSXM.PageObject.CrossingManagement.StraightLoad_StraightLif_tManagement import \
    StraightLoad_StraightLift_Management
from GTOSXM.TestCase.Interface_Test.InterfacePage import Interface_Page

req = RequestHandler()
login_res = req.visit("post", url=configinterface.url, json=configinterface.BodyXRCT)
login_text = login_res.json()
assert login_text['result'] == 0
a = login_text['data']['Token']
Authorization = 'Bearer ' + a
configinterface.head['Authorization'] = a


# @pytest.mark.skipif
# @pytest.mark.parametrize("input", read_yaml('direct_loadingp_rocess.yaml'))
@allure.story('7.大船直装流程')
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
@allure.story('7.大船直装流程')
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


# @pytest.mark.skip
@allure.story('7.大船直装流程')
@allure.title('3.有结构船舶配载')
@pytest.mark.parametrize("input",
                         read_yaml(os.path.join(os.getcwd(), '07_DirectLoadingProcess', 'direct_loadingp_rocess.yaml')))
def testship_stowage(driver, input):
    """有结构配载"""
    menu = GtosMenu(driver)
    menu.select_level_Menu("船舶策划,有结构船舶配载")
    stowage = Structure_Stowage(driver)
    stowage.Retrieve(input)
    stowage.mouse_job()
    stowage.choice_table()
    htps = Interface_Page(driver)
    # 定义船箱位接口
    htps.modify_position('010982')
    # #配载接口
    htps.interface_getboxno(config.boxNumberThree)
    peizai = req.visit('post', url=read_yaml(os.path.join('../Interface_Test', 'interface.yaml'))[0]['配载url'],
                       data=json.dumps(read_json(os.path.join(os.getcwd(), '../Interface_Test/json', 'peizai.json'))),
                       headers=configinterface.head)
    stowage.mouse_job_once()
    stowage.send_box()
    Tag(driver).closeTagGtos('有结构船舶配载')


# @pytest.mark.skipif
# @pytest.mark.parametrize("input", read_yaml('direct_loadingp_rocess.yaml'))
@allure.story('7.大船直装流程')
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
# @pytest.mark.parametrize("input", read_yaml('direct_liftin_process.yaml'))
@allure.story('7.大船直装流程')
@allure.title('5、有结构船舶监控允许直装')
@pytest.mark.parametrize("input",
                         read_yaml(os.path.join(os.getcwd(), '06_DirectLiftingProcess', 'direct_liftin_process.yaml')))
def testLifting(driver, input):
    """有结构船舶允许直提"""
    menu = GtosMenu(driver)
    menu.select_level_Menu("船舶监控,有结构船舶监控")
    send_box = Structure_Monitoring(driver)
    send_box.Retrieve(input, config.importNumber)
    send_box.mouse_job()
    # 切换窗口
    cls = driver.window_handles
    driver.switch_to.window(cls[1])
    send_box.new_windows_choicebox(config.boxNumberThree)
    send_box.new_windows_job()
    send_box.direct_job('直装', '允许直装')
    send_box.selective_bridge(config.boxNumberThree)
    driver.close()
    # 切回原来窗口
    driver.switch_to.window((cls[0]))
    Tag(driver).closeTagGtos('有结构船舶监控')


# @pytest.mark.skipif
@allure.story('7.大船直装流程')
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


# @pytest.mark.skipif
@allure.story('7.大船直装流程')
@allure.title('7、车辆出场')
@pytest.mark.parametrize("input",
                         read_yaml(os.path.join(os.getcwd(), '07_DirectLoadingProcess', 'direct_loadingp_rocess.yaml')))
def testCar_Out(driver, input):
    """车辆出场"""
    menu = GtosMenu(driver)
    menu.select_level_Menu("道口管理,车辆出场")
    car_out = Car_Out(driver)
    car_out.input_values(input)
    car_out.retrieve()
    car_out.confirm_out_loadingAndLifting()
    Tag(driver).closeTagGtos('车辆出场')


if __name__ == '__main__':
    pytest.main(['-sv'])
