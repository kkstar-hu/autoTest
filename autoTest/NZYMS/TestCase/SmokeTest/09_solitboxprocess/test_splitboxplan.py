import os
import time

import allure

from Commons.Controls.tag import Tag
from Commons.menu import Menu
from Commons.yamlread import read_yaml
from Commons import allurechange
from NZYMS.PageObject.CrossingManagement.Out_confirm import Out_Confirm
from NZYMS.PageObject.CrossingManagement.cars_registration import Cars_Registration
from NZYMS.PageObject.MarketingDepartmentManagement.Send_Mention_CarOut import Send_Mention_CarOut
from NZYMS.PageObject.MarketingDepartmentManagement.Split_box_Confirm import Split_Box_Confirm
from NZYMS.PageObject.MarketingDepartmentManagement.Split_box_Plan import Split_Box_Plan
from NZYMS.PageObject.Query_Statistics.Storage_box_query import Storage_Box_Query
import pytest as pytest


# @allure.epic('拆箱计划')
# @allure.title('获取箱内信息成功')
# @allure.story('获取箱内信息')
# # @pytest.mark.skipif
# # @pytest.mark.parametrize("input", read_yaml('split_box.yaml'))
# @pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(),'09_solitboxprocess','split_box.yaml')))
# def testGet_information(driver, input):
#     """获取计划箱信息"""
#     menu = Menu(driver)
#     menu.select_level_Menu("查询统计,存场箱查询")
#     stor_box_query = Storage_Box_Query(driver)
#     stor_box_query.select_body(input)
#     stor_box_query.get_information()
#     Tag(driver).closeTag("存场箱查询")


@allure.title('1.新增拆箱计划')
@allure.story('9、拆箱计划流程')
# @pytest.mark.skipif
# @pytest.mark.parametrize("input", read_yaml('split_box.yaml'))
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(),'09_solitboxprocess','split_box.yaml')))
def testSplit_Plan(driver, input):
    """拆箱计划"""
    menu = Menu(driver)
    menu.select_level_Menu("仓储管理,拆箱管理,拆箱计划")
    split_box = Split_Box_Plan(driver)
    split_box.addPlan(input)

@allure.title('2.新增箱信息和车辆信息')
@allure.story('9、拆箱计划流程')
# @pytest.mark.skipif
# @pytest.mark.parametrize("input", read_yaml('split_box.yaml'))
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(), '09_solitboxprocess', 'split_box.yaml')))
def testSplit_PlanAddBox(driver, input):
    split_box = Split_Box_Plan(driver)
    split_box.addBoxPlan(input)
    split_box.switch_goods_information()
    split_box.addCar(input)
    split_box.perform_tasks()
    Tag(driver).closeTag("拆箱计划")

@allure.title('3.拆箱车辆进场')
@allure.story('9、拆箱计划流程')
# @pytest.mark.skipif
# @pytest.mark.parametrize("input", read_yaml('split_box.yaml'))
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(),'09_solitboxprocess','split_box.yaml')))
def testSplit_into_car(driver,input):
    """拆箱车辆进场"""
    menu = Menu(driver)
    menu.select_level_Menu("道口管理,车辆进场登记")
    cars_into = Cars_Registration(driver)
    cars_into.out_process(input)
    Tag(driver).closeTag("车辆进场登记")

@allure.title('4.拆箱确认')
@allure.story('9、拆箱计划流程')
# @pytest.mark.skipif
# @pytest.mark.parametrize("input", read_yaml('split_box.yaml'))
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(),'09_solitboxprocess','split_box.yaml')))
def testSplit_Confirm(driver, input):
    """拆箱确认"""
    menu = Menu(driver)
    menu.select_level_Menu("仓储管理,拆箱管理,拆箱确认")
    split_confirm = Split_Box_Confirm(driver)
    split_confirm.addBOX_information(input)
    Tag(driver).closeChoiceTag("拆箱确认")

@allure.title('5.拆箱货车确认放行')
@allure.story('9、拆箱计划流程')
# @pytest.mark.skipif
# @pytest.mark.parametrize("input", read_yaml('split_box.yaml'))
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(),'09_solitboxprocess','split_box.yaml')))
def testSendMention(driver,input):
    """拆箱货车确认放行"""
    menu = Menu(driver)
    menu.select_level_Menu("仓储管理,送提货车放行确认")
    send_and_mention = Send_Mention_CarOut(driver)
    send_and_mention.process(input)
    Tag(driver).closeTag("送提货车放行确认")

@allure.title('6.车辆出场')
@allure.story('9、拆箱计划流程')
# @pytest.mark.skipif
# @pytest.mark.parametrize("input", read_yaml('split_box.yaml'))
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(),'09_solitboxprocess','split_box.yaml')))
def testSend_Box_Out_Confirm(driver, input):
    """车辆出场"""
    menu = Menu(driver)
    menu.select_level_Menu("道口管理,出场确认")
    out_confirm = Out_Confirm(driver)
    out_confirm.out_confirm(input)
    out_confirm.choice_car(input)
    out_confirm.confirm_button()
    Tag(driver).closeTag("出场确认")

if __name__ == '__main__':
    # pytest.main(['-v','--alluredir','./result','--clean-alluredir','test_outplan.py'])
    # os.system('allure generate ./result -o ./report --clean')
    # allurechange.set_windos_title('集疏运UI自动化测试')
    # report_title = allurechange.get_json_data("集疏运测试报告")
    # allurechange.write_json_data(report_title)
    pytest.main(['-sv'])