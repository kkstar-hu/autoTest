import os
import allure
import pytest as pytest
import pytest_check as check
from Base.baseinterface import RequestHandler
from Commons.Controls.tag import Tag
from Commons.yamlread import read_yaml
from GTOSXM.Config import config, configinterface
from GTOSXM.PageObject.Control_Ship.Structure_Monitoring import Structure_Monitoring
from GTOSXM.PageObject.DataManagement.ExitInformation_manifest import Manifest
from GTOSXM.PageObject.Mechanical_Control.Inset_Car import Inset_Car
from GTOSXM.PageObject.Mechanical_Control.Job_Order_Monitoring import Job_Order_Monitoring
from GTOSXM.PageObject.Ship_Planning.Structure_Stowage import Structure_Stowage
from GTOSXM.PageObject.gtos_menu import GtosMenu
from GTOSXM.TestCase.Interface_Test.InterfacePage import Interface_Page

req = RequestHandler()
login_res = req.visit("post", url=configinterface.loginurl, json=configinterface.BodyXRCT)
login_text = login_res.json()
assert login_text['result'] == 0
a = login_text['data']['Token']
Authorization = 'Bearer ' + a
configinterface.head['Authorization'] = a


# @pytest.mark.skip
@allure.story('5.大船装船流程')
@allure.title('1.装船箱放行')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(), '05_PutBoxIntoShipProcess', 'loadship.yaml')))
def testCheckInBox(driver, input):
    menu = GtosMenu(driver)
    menu.select_level_Menu("资料管理,出口资料,装船箱放行")
    Load = Manifest(driver)
    Load.search()
    Load.permitthrough()


# @pytest.mark.skip
@allure.story('5.大船装船流程')
@allure.title('2.有结构船舶配载')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(), '05_PutBoxIntoShipProcess', 'loadship.yaml')))
def testship_stowage(driver, input):
    """有结构配载"""
    menu = GtosMenu(driver)
    menu.select_level_Menu("船舶策划,有结构船舶配载")
    stowage = Structure_Stowage(driver)
    stowage.Retrieve(input)
    stowage.mouse_job()
    htps = Interface_Page(driver)
    # 配载接口
    boxid = htps.interface_getboxno(config.outBoxNumber)[0]
    voyid = htps.interface_getboxno(config.outBoxNumber)[1]
    peizaijson={"LogID": 0, "VoyID": voyid, "StowageMode": "1", "Direction": "2",
     "StowageLocs": [{"VoyID": voyid, "VLocation": "010582", "BigNo": "02", "SeqNo": 1, "HatchID": 143473}],
     "StowageContainers": [{"ContainerID": boxid}]}
    peizai = req.visit('post', url=configinterface.url+"/api/vesselload/Stowage",
                       json=peizaijson,
                       headers=configinterface.head)

    stowage.mouse_job_once()
    stowage.send_box()
    Tag(driver).closeTagGtos('有结构船舶配载')


# @pytest.mark.skipif
@allure.story('5.大船装船流程')
@allure.title('3、大船发箱')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(), '05_PutBoxIntoShipProcess', 'loadship.yaml')))
def testShip_sendbox(driver, input):
    """大船发箱"""
    menu = GtosMenu(driver)
    menu.select_level_Menu("船舶监控,有结构船舶监控")
    nostructure = Structure_Monitoring(driver)
    nostructure.Retrieve(input, config.importNumber)
    nostructure.mouse_job()
    # 切换窗口
    cls = driver.window_handles
    driver.switch_to.window(cls[1])
    nostructure.new_windows_choicebox(config.outBoxNumber)
    nostructure.new_windows_job()
    nostructure.new_windows_sendbox()
    nostructure.selective_bridge(config.outBoxNumber)
    driver.close()
    # 切回原来窗口
    driver.switch_to.window((cls[0]))
    Tag(driver).closeTagGtos('有结构船舶监控')


# @pytest.mark.skip
@allure.story('5.大船装船流程')
@allure.title('4、内集卡控制')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(), '05_PutBoxIntoShipProcess', 'loadship.yaml')))
def testCharge_Car(driver, input):
    """查看内集卡"""
    menu = GtosMenu(driver)
    menu.select_level_Menu("机械控制,内集卡控制")
    inset_car = Inset_Car(driver)
    inset_car.choice_job('AUT')
    inset_car.choice_cars('作业步骤', '等待装车')
    Tag(driver).closeTagGtos('内集卡控制')


# @pytest.mark.skip
@allure.story('5.大船装船流程')
@allure.title('5.作业指令监控')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(), '05_PutBoxIntoShipProcess', 'loadship.yaml')))
def testship_order(driver, input):
    """作业指令监控"""
    menu = GtosMenu(driver)
    menu.select_level_Menu("机械控制,作业指令监控")
    work = Job_Order_Monitoring(driver)
    work.Retrieve(input,shipname=None,boxnumber=config.outBoxNumber)
    work.order_info_check(input, config.outBoxNumber)
    work.charge_car(input)
    work.send_box(input)
    work.LadeShip_confirm(input)
    Tag(driver).closeTagGtos('作业指令监控')

