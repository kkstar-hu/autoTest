import os
import allure
import pytest
from BTOSLJ.Config import config
from BTOSLJ.PageObject.store_management.Import_store_bill_management import ImStoreBill
from Commons.menu import Menu
from Commons.yamlread import read_yaml


@allure.story('一、卸船流程')
@allure.title('1.新增仓单')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(), 'unship.yaml')))
def test_add_store_bill(driver, input):
    menu = Menu(driver)
    menu.select_level_Menu("仓库管理,内贸进口仓库管理,内贸进口舱单管理")
    ship_bill = ImStoreBill(driver)
    ship_bill.add_bill(config.importNumber, input)
    ship_bill.check_table_bill(input)
    ship_bill.check_table_goods(input)
