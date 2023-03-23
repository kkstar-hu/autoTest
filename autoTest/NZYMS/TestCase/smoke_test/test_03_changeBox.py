import os.path
import time

import allure
import pytest as pytest
from Commons.Controls.tag import Tag
from Commons.menu import Menu
from Commons.yamlread import read_yaml
from NZYMS.config import config
from NZYMS.PageObject.BoxManagement.changebox import ChangeBox
from NZYMS.PageObject.PayManagement.Settlement_charge import Settlement_Charge

@allure.story('3.集装箱整改流程')
@allure.title('1.添加集装箱整改计划')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(),'03_changeBoxProcess','changebox.yaml')))
def testchangebox(driver,input):
    menu=Menu(driver)
    menu.select_level_Menu("箱务管理,集装箱整改")
    changebox=ChangeBox(driver)
    changebox.search(input)
    changebox.checkboxInformation(input)
    changebox.addchangePlan(input)
    Tag(driver).closeTag("集装箱整改")
@allure.story('3.集装箱整改流程')
@allure.title('2.整改计划结算')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(),'03_changeBoxProcess','changebox.yaml')))
def testchargepay(driver,input):
    menu = Menu(driver)
    menu.select_level_Menu("费收管理,费用管理,结算收费")
    charge = Settlement_Charge(driver)
    charge.search(config.boxNumber, "20/整改计划")
    charge.check_change_box_information(input)
    charge.configuration()
    charge.pay(input)
    driver.refresh()
    time.sleep(1)





if __name__ == '__main__':
    pytest.main(['-vs','--alluredir','../allure-result'])
    #os.system('allure generate ../allure-result -o ../reports')