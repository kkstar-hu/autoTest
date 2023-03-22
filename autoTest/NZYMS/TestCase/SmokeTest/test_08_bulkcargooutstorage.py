import os.path
import allure
from Commons.Controls.tag import Tag
from Commons.menu import Menu
from Commons.yamlread import read_yaml
from NZYMS.Config import config
from NZYMS.PageObject.CrossingManagement.Out_confirm import Out_Confirm
from NZYMS.PageObject.CrossingManagement.cars_registration import Cars_Registration
from NZYMS.PageObject.MarketingDepartmentManagement.Bulk_cargo_out_storageConfirm import Bulk_cargo_out_storageConfirm
from NZYMS.PageObject.MarketingDepartmentManagement.Bulk_cargo_out_storagePlan import Bulk_cargo_out_storagePlan
from NZYMS.PageObject.MarketingDepartmentManagement.Send_Mention_CarOut import Send_Mention_CarOut
import pytest as pytest
from NZYMS.PageObject.Query_Statistics.out_storage_query import Out_Storage_Query


@allure.title('1.新增散货出库计划')
@allure.story('7、散货出库计划')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(), '08_bulkcargooutstorage', 'bulk_out.yaml')))
def testBulk_out(driver, input):
    """散货出库计划"""
    menu = Menu(driver)
    menu.select_level_Menu("仓储管理,出库管理,散货出库计划")
    bulk_out = Bulk_cargo_out_storagePlan(driver)
    bulk_out.addPlan(input)

@allure.title('2.新增箱信息和车辆信息')
@allure.story('7、散货出库计划')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(), '08_bulkcargooutstorage', 'bulk_out.yaml')))
def testBulk_outaddbox(driver, input):
    bulk_out = Bulk_cargo_out_storagePlan(driver)
    bulk_out.addBox(input)
    bulk_out.switch_car_information()
    bulk_out.addCar(input)
    bulk_out.perform_tasks()
    Tag(driver).closeChoiceTag("散货出库计划")


# @pytest.mark.parametrize("input", read_yaml("bulk_out.yaml"))
@allure.title('3.散货出库车辆进场')
@allure.story('7、散货出库计划')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(), '08_bulkcargooutstorage', 'bulk_out.yaml')))
def testBulk_out_car(driver,input):
    """散货出库车辆进场"""
    menu = Menu(driver)
    menu.select_level_Menu("道口管理,车辆进场登记")
    cars_into = Cars_Registration(driver)
    cars_into.out_process(input)
    Tag(driver).closeTag("车辆进场登记")

@allure.title('4.散货出库确认')
@allure.story('7、散货出库计划')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(), '08_bulkcargooutstorage', 'bulk_out.yaml')))
def testBulk__outconfirm(driver, input):
    """散货出库确认"""
    menu = Menu(driver)
    menu.select_level_Menu("仓储管理,出库管理,散货出库确认")
    bulk_out_confirm = Bulk_cargo_out_storageConfirm(driver)
    bulk_out_confirm.addbulk_out(input)
    Tag(driver).closeTag("散货出库确认")

@allure.title('5.散货出库车辆放行')
@allure.story('7、散货出库计划')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(), '08_bulkcargooutstorage', 'bulk_out.yaml')))
def testSendMention(driver,input):
    """送提货车确认放行"""
    menu = Menu(driver)
    menu.select_level_Menu("仓储管理,送提货车放行确认")
    send_and_mention = Send_Mention_CarOut(driver)
    send_and_mention.process(input)
    Tag(driver).closeTag("送提货车放行确认")

@allure.title('6.散货入库车辆出场')
@allure.story('7、散货出库计划')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(), '08_bulkcargooutstorage', 'bulk_out.yaml')))
def testSend_Box_Out_Confirm(driver, input):
    """车辆出场"""
    menu = Menu(driver)
    menu.select_level_Menu("道口管理,出场确认")
    out_confirm = Out_Confirm(driver)
    out_confirm.out_confirm(input)
    out_confirm.choice_car(input)
    out_confirm.confirm_button()
    Tag(driver).closeTag("出场确认")

@allure.title('7.市场部查询-出库流程查询')
@allure.story('7.散货出库计划')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(), '08_bulkcargooutstorage', 'bulk_out.yaml')))
def test_search_outStorage(driver, input):
    """车辆出场"""
    menu = Menu(driver)
    menu.select_level_Menu("查询统计,市场部查询,出库查询")
    search = Out_Storage_Query(driver)
    search.search_and_check(input, config.bulkoutNumber)
    Tag(driver).closeTag("出库查询")


