import os

import allure
import pytest

from BTOSLJ.Controls.BTOS_menu import BtosMenu
from BTOSLJ.PageObject.tallyman.tallyman_manage import Tallyman
from Commons.yamlread import read_yaml


@allure.story('一、卸船流程')
@allure.title('5.理货员出勤')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(), 'tallyman_data.yaml')))
def test_05_Tallyman_Out_For_Work(driver, input: dict):
    print("******************************************Smoke Test Start***********************************************")
    menu = BtosMenu(driver)
    menu.select_level2_menu("仓库管理", "理货员出勤")
    tallyman = Tallyman(driver)
    tallyman.Out_For_Work(input)
