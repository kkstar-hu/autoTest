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
from NZYMS.PageObject.Query_Statistics.Storage_box_query import Storage_Box_Query
from NZYMS.PageObject.MarketingDepartmentManagement.Packing_Plan import Packing_Plan
from NZYMS.PageObject.MarketingDepartmentManagement.Packing_Confirm import Packing_Confirm
import pytest as pytest


# @allure.epic('装箱计划')
# @allure.title('获取箱内信息成功')
# @allure.story('获取箱内信息')
# # @pytest.mark.skipif
# # @pytest.mark.parametrize("input", read_yaml('packing_box_new.yaml'))
# @pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(),'08_packingboxprocess','packing_box_new.yaml')))
# def testGet_information(driver, input):
#     """获取计划箱信息"""
#     menu = Menu(driver)
#     menu.select_level_Menu("查询统计,存场箱查询")
#     stor_box_query = Storage_Box_Query(driver)
#     stor_box_query.select_body(input)
#     #stor_box_query.get_information(1)
#     Tag(driver).closeTag("存场箱查询")


@allure.title('1.新增装箱计划')
@allure.story('3、装箱计划库内追加流程')
# @pytest.mark.skipif
# @pytest.mark.parametrize("input", read_yaml('packing_box_new.yaml'))
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(),'08_packingboxprocess', 'packing_box_warehouse.yaml')))
def testPacking_Plan(driver, input):
    """装箱计划"""
    menu = Menu(driver)
    menu.select_level_Menu("市场部管理,装箱管理,装箱计划")
    packing_plan = Packing_Plan(driver)
    packing_plan.addPlan(input)



@allure.title('2.新增箱子信息和货信息')
@allure.story('3、装箱计划库内追加流程')
# @pytest.mark.skipif
# @pytest.mark.parametrize("input", read_yaml('packing_box_new.yaml'))
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(), '08_packingboxprocess', 'packing_box_warehouse.yaml')))
def testPacking_PlanAddbox(driver, input):
    packing_plan = Packing_Plan(driver)
    packing_plan.addBoxPlan(input)
    packing_plan.switch_goods_information()
    packing_plan.addGoods_warehouse(input)
    packing_plan.perform_tasks()
    Tag(driver).closeChoiceTag("装箱计划")



@allure.title('3.装箱确认')
@allure.story('3、装箱计划库内追加流程')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(),'08_packingboxprocess', 'packing_box_warehouse.yaml')))
def testPacking_Confirm(driver, input):
    """装箱确认"""
    menu = Menu(driver)
    menu.select_level_Menu("市场部管理,装箱管理,装箱确认")
    packing_confirm = Packing_Confirm(driver)
    packing_confirm.addBOX_information(input)
    Tag(driver).closeTag("装箱确认")




#
#
# if __name__ == '__main__':
#     # pytest.main(['-v','--alluredir','./result','--clean-alluredir','test_outplan.py'])
#     # os.system('allure generate ./result -o ./report --clean')
#     # allurechange.set_windos_title('集疏运UI自动化测试')
#     # report_title = allurechange.get_json_data("集疏运测试报告")
#     # allurechange.write_json_data(report_title)
#     pytest.main(['-sv'])