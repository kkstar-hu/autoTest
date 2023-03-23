import os.path
import allure

from Commons import allurechange
from Commons.Controls.tag import Tag
from Commons.menu import Menu
from Commons.yamlread import read_yaml
from NZYMS.config import config
from NZYMS.PageObject.CrossingManagement.Out_confirm import Out_Confirm
from NZYMS.PageObject.CrossingManagement.cars_registration import Cars_Registration
from NZYMS.PageObject.MarketingDepartmentManagement.Bulk_cargo_into_storageConfirm import Bulk_cargo_into_storageConfirm
from NZYMS.PageObject.MarketingDepartmentManagement.Send_Mention_CarOut import Send_Mention_CarOut
from NZYMS.PageObject.MarketingDepartmentManagement.Bulk_cargo_into_storagePlan import Bulk_cargo_into_storagePlan
import pytest as pytest
from NZYMS.PageObject.Query_Statistics.into_storage_query import Into_Storage_Query


@allure.title('1.新增散货入库计划')
@allure.story('6.散货入库计划流程')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(), '07_bulkcargointostorage', 'bulk_into.yaml')))
def testBulk_into(driver, input):
    """散货入库计划"""
    menu = Menu(driver)
    menu.select_level_Menu("仓储管理,入库管理,散货入库计划")
    bulk_into = Bulk_cargo_into_storagePlan(driver)
    bulk_into.addPlan(input)

@allure.title('2.新增散货入库箱信息和车辆信息')
@allure.story('6.散货入库计划流程')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(), '07_bulkcargointostorage', 'bulk_into.yaml')))
def testBulk_intoaddbox(driver, input):
    bulk_into = Bulk_cargo_into_storagePlan(driver)
    bulk_into.addBox(input)
    bulk_into.switch_car_information()
    bulk_into.addCar(input)
    bulk_into.perform_tasks()
    Tag(driver).closeTag("散货入库计划")

@allure.title('3.散货入库车辆进场')
@allure.story('6.散货入库计划流程')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(), '07_bulkcargointostorage', 'bulk_into.yaml')))
def testBulk_into_car(driver,input):
    """散货入库车辆进场"""
    menu = Menu(driver)
    menu.select_level_Menu("道口管理,车辆进场登记")
    cars_into = Cars_Registration(driver)
    cars_into.into_process(input)
    Tag(driver).closeTag("车辆进场登记")

@allure.title('4.散货入库确认')
@allure.story('6.散货入库计划流程')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(), '07_bulkcargointostorage', 'bulk_into.yaml')))
def testBulk_into_confirm(driver, input):
    """散货入库"""
    menu = Menu(driver)
    menu.select_level_Menu("仓储管理,入库管理,散货入库确认")
    bulk_into_confirm = Bulk_cargo_into_storageConfirm(driver)
    bulk_into_confirm.addbulk_into(input)
    Tag(driver).closeTag("散货入库确认")

@allure.title('5.散货入库车辆放行')
@allure.story('6.散货入库计划流程')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(), '07_bulkcargointostorage', 'bulk_into.yaml')))
def testSendMention(driver,input):
    """送提货车确认放行"""
    menu = Menu(driver)
    menu.select_level_Menu("仓储管理,送提货车放行确认")
    send_and_mention = Send_Mention_CarOut(driver)
    send_and_mention.process(input)
    Tag(driver).closeTag("送提货车放行确认")

@allure.title('6.散货入库车辆出场')
@allure.story('6.散货入库计划流程')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(), '07_bulkcargointostorage', 'bulk_into.yaml')))
def testSend_Box_Out_Confirm(driver, input):
    """车辆出场"""
    menu = Menu(driver)
    menu.select_level_Menu("道口管理,出场确认")
    out_confirm = Out_Confirm(driver)
    out_confirm.out_confirm(input)
    out_confirm.choice_car(input)
    out_confirm.confirm_button()
    Tag(driver).closeTag("出场确认")

@allure.title('7.市场部查询-入库流程查询')
@allure.story('6.散货入库计划流程')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(), '07_bulkcargointostorage', 'bulk_into.yaml')))
def test_search_intoStorage(driver, input):
    """车辆出场"""
    menu = Menu(driver)
    menu.select_level_Menu("查询统计,市场部查询,入库查询")
    search = Into_Storage_Query(driver)
    search.search_and_check(input, config.bulkintoNumber)
    Tag(driver).closeTag("入库查询")

if __name__ == '__main__':
    pytest.main([
        '../smoke_test/test_bulkcargointostorage.py',
        '-sv', '--alluredir', '../../report/result', "--clean-alluredir"])


    os.system('allure generate ../../report/result -o ../../report/html --clean')
    allurechange.set_windos_title('集疏运UI自动化测试')
    report_title = allurechange.get_json_data("集疏运测试报告")
    allurechange.write_json_data(report_title)