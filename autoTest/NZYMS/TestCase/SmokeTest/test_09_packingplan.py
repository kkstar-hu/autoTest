import os
import allure
from Commons.Controls.tag import Tag
from Commons.menu import Menu
from Commons.yamlread import read_yaml
from Commons import allurechange
from NZYMS.PageObject.CrossingManagement.Out_confirm import Out_Confirm
from NZYMS.PageObject.CrossingManagement.cars_registration import Cars_Registration
from NZYMS.PageObject.MarketingDepartmentManagement.Send_Mention_CarOut import Send_Mention_CarOut
from NZYMS.PageObject.Query_Statistics.Storage_box_query import Storage_Box_Query
from NZYMS.PageObject.MarketingDepartmentManagement.Packing_Plan import Packing_Plan
from NZYMS.PageObject.MarketingDepartmentManagement.Packing_Confirm import Packing_Confirm
import pytest as pytest


# @pytest.mark.skipif
@allure.title('1.新增装箱计划')
@allure.story('8、装箱计划流程')
# @pytest.mark.parametrize("input", read_yaml('packing_box_new.yaml'))
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(), '09_packingboxprocess', 'packing_box_new.yaml')))
def testPacking_Plan(driver, input):
    """装箱计划"""
    menu = Menu(driver)
    menu.select_level_Menu("仓储管理,装箱管理,装箱计划")
    packing_plan = Packing_Plan(driver)
    packing_plan.addPlan(input)


@allure.title('2.新增箱子信息和货信息')
@allure.story('8、装箱计划流程')
# @pytest.mark.parametrize("input", read_yaml('packing_box_new.yaml'))
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(), '09_packingboxprocess', 'packing_box_new.yaml')))
def testPacking_PlanAddbox(driver, input):
    packing_plan = Packing_Plan(driver)
    packing_plan.addBoxPlan(input)
    packing_plan.switch_goods_information()
    packing_plan.addGoods_stow(input)
    packing_plan.addGoods_warehouse(input)
    packing_plan.perform_tasks()
    Tag(driver).closeChoiceTag("装箱计划")

@allure.title('3.装箱车辆进场')
@allure.story('8、装箱计划流程')
# @pytest.mark.parametrize("input", read_yaml('packing_box_new.yaml'))
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(), '09_packingboxprocess', 'packing_box_new.yaml')))
def testPacking_into_car(driver,input):
    """装箱车辆进场"""
    menu = Menu(driver)
    menu.select_level_Menu("道口管理,车辆进场登记")
    car_process = Cars_Registration(driver)
    car_process.into_process(input)
    Tag(driver).closeTag("车辆进场登记")


@allure.title('4.装箱确认')
@allure.story('8、装箱计划新流程')
# @pytest.mark.parametrize("input", read_yaml('packing_box_new.yaml'))
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(), '09_packingboxprocess', 'packing_box_new.yaml')))
def testPacking_Confirm(driver, input):
    """装箱确认"""
    menu = Menu(driver)
    menu.select_level_Menu("仓储管理,装箱管理,装箱确认")
    packing_confirm = Packing_Confirm(driver)
    packing_confirm.addBOX_information(input)
    Tag(driver).closeTag("装箱确认")


# @pytest.mark.skipif
@allure.title('5.装箱货车放行')
@allure.story('8、装箱计划流程')
# @pytest.mark.parametrize("input", read_yaml('packing_box_new.yaml'))
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(), '09_packingboxprocess', 'packing_box_new.yaml')))
def testSendMention(driver,input):
    """装箱货车确认放行"""
    menu = Menu(driver)
    menu.select_level_Menu("仓储管理,送提货车放行确认")
    send_and_mention = Send_Mention_CarOut(driver)
    send_and_mention.process(input)
    Tag(driver).closeTag("送提货车放行确认")


# @pytest.mark.skipif
@allure.title('6.装箱货车出场')
@allure.story('8、装箱计划流程')
# @pytest.mark.parametrize("input", read_yaml('packing_box_new.yaml'))
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(), '09_packingboxprocess', 'packing_box_new.yaml')))
def testSend_Box_Out_Confirm(driver, input):
    """车辆出场"""
    menu = Menu(driver)
    menu.select_level_Menu("道口管理,出场确认")
    out_confirm = Out_Confirm(driver)
    out_confirm.out_confirm(input)
    out_confirm.choice_car(input)
    out_confirm.confirm_button()
    Tag(driver).closeTag("出场确认")


#

if __name__ == '__main__':
    # pytest.main(['-v','--alluredir','./result','--clean-alluredir','test_outplan.py'])
    # os.system('allure generate ./result -o ./report --clean')
    # allurechange.set_windos_title('集疏运UI自动化测试')
    # report_title = allurechange.get_json_data("集疏运测试报告")
    # allurechange.write_json_data(report_title)
    pytest.main(['-sv'])