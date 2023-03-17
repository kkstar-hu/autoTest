import json
import os
import allure
import pytest as pytest
from Base.baseinterface import RequestHandler
from Commons.Controls.tag import Tag
from Commons.jsonread import read_json
from Commons.yamlread import read_yaml
from GTOS.Config import config, configinterface
from GTOS.PageObject.Control_Ship.Structure_Monitoring import Structure_Monitoring
from GTOS.PageObject.DataManagement.ExitInformation_manifest import Manifest
from GTOS.PageObject.Mechanical_Control.Inset_Car import Inset_Car
from GTOS.PageObject.Mechanical_Control.Job_Order_Monitoring import Job_Order_Monitoring
from GTOS.PageObject.Ship_Planning.Structure_Stowage import Structure_Stowage
from GTOS.PageObject.gtos_menu import GtosMenu
from GTOS.TestCase.Interface_Test.InterfacePage import testinterface_getboxno

req = RequestHandler()
login_res = req.visit("post", url=configinterface.url, json=configinterface.BodyA)
login_text = login_res.json()
assert login_text['result'] == 0
a = login_text['data']['Token']
Authorization = 'Bearer ' + a
configinterface.head['Authorization'] = a

# @pytest.mark.skip
@allure.story('5.装船流程')
@allure.title('1.装船箱放行')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(),'05_PutBoxIntoShipProcess','loadship.yaml')))
def testCheckInBox(driver,input):
    menu = GtosMenu(driver)
    menu.select_level_Menu("资料管理,出口资料,装船箱放行")
    Load=Manifest(driver)
    Load.search()
    Load.permitthrough()


# @pytest.mark.skip
@allure.story('5.装船流程')
@allure.title('2.有结构船舶配载')
@pytest.mark.parametrize("input",read_yaml(os.path.join(os.getcwd(),'01_DataProcess','immediata_plan.yaml')))
def testship_stowage(driver, input):
    """有结构配载"""
    menu = GtosMenu(driver)
    menu.select_level_Menu("船舶策划,有结构船舶配载")
    stowage = Structure_Stowage(driver)
    stowage.Retrieve(input)
    #配载接口
    testinterface_getboxno(config.outBoxNumber)
    peizai = req.visit('post',url = read_yaml(r'D:\ATA\autoTest\GTOS\TestCase\Interface_Test\interface.yaml')[0]['配载url'],
                       data = json.dumps(read_json(r'D:\ATA\autoTest\GTOS\TestCase\Interface_Test\JSOn\peizai.json')),
                       headers=configinterface.head)
    stowage.refresh_peizai()
    Tag(driver).closeTagGtos('有结构船舶配载')


# @pytest.mark.skipif
@allure.story('2.大船卸船流程')
@allure.title('4、大船发箱')
@pytest.mark.parametrize("input",read_yaml(os.path.join(os.getcwd(),'01_DataProcess','immediata_plan.yaml')))
def testShip_sendbox(driver, input):
    """大船发箱"""
    menu = GtosMenu(driver)
    menu.select_level_Menu("船舶监控,有结构船舶监控")
    nostructure = Structure_Monitoring(driver)
    nostructure.Retrieve(input)
    #作业顺序接口
    jobshunxu = req.visit('post',url = read_yaml(r'D:\ATA\autoTest\GTOS\TestCase\Interface_Test\interface.yaml')[0]['作业顺序url'],
                    data = json.dumps(read_json(r'D:\ATA\autoTest\GTOS\TestCase\Interface_Test\JSOn\zuoyeshunxu.json')),
                    headers = configinterface.head)
    nostructure.LadeShip_Send_Box(config.outBoxNumber)
    Tag(driver).closeTagGtos('有结构船舶监控')



# @pytest.mark.skip
@allure.story('5.装船流程')
@allure.title('3、内集卡控制')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(),'05_PutBoxIntoShipProcess','loadship.yaml')))
def testCharge_Car(driver, input):
    """查看内集卡"""
    menu = GtosMenu(driver)
    menu.select_level_Menu("机械控制,内集卡控制")
    inset_car = Inset_Car(driver)
    inset_car.choice_job('A02')
    inset_car.choice_cars('作业步骤','空车')
    Tag(driver).closeTagGtos('内集卡控制')


# @pytest.mark.skip
@allure.story('5.装船流程')
@allure.title('5.作业指令监控')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(),'05_PutBoxIntoShipProcess','loadship.yaml')))
def testship_order(driver, input):
    """作业指令监控"""
    menu = GtosMenu(driver)
    menu.select_level_Menu("机械控制,作业指令监控")
    work = Job_Order_Monitoring(driver)
    work.Retrieve(input,config.outportNumber,config.outBoxNumber)
    work.order_info_check(input,config.outBoxNumber)
    work.charge_car(input)
    work.send_box(input)
    work.LadeShip_confirm(input)
    Tag(driver).closeTagGtos('作业指令监控')

if __name__ == '__main__':
    #pytest.main(['-vs'])
    pytest.main(['-s', '-v', 'test_EnterBoxProcess.py','--html=../report/report.html', '--alluredir','../report/allure-results'])