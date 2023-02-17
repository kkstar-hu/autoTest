import os

import allure
import pytest as pytest

from Commons.Controls.tag import Tag
from Commons.menu import Menu
from Commons.yamlread import read_yaml
from NZYMS.Config import config
from NZYMS.PageObject.CenterControlManagement.changeStorePlan import ChangeStorePlan
from NZYMS.PageObject.CenterControlManagement.car_load import Car_Load


#@pytest.mark.skip
@allure.story('2.转堆流程')
@allure.title('1.添加转堆计划')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(),'02_changeStoreProcess','changeStorePlan.yaml')))
def testAddChangeStorePlan(driver, input):
    menu=Menu(driver)
    menu.select_level_Menu("中控管理,场内计划管理,转堆计划管理")
    changeStorePlan=ChangeStorePlan(driver)
    changeStorePlan.addChangePlan(input,config.boxNumber)
    #changeStorePlan.addWorkOrder(input,"JX_516784")
    Tag(driver).closeTag("转堆计划管理")

@allure.story('2.转堆流程')
@allure.title('2.车载中转推操作')
def testChangeStore(driver):
    menu=Menu(driver)
    menu.select_level_Menu("中控管理,车载")
    changebox=Car_Load(driver)
    changebox.switchNewWindow()
    changebox.changeStore("FZ/辅助区堆场","重箱")
    changebox.choice_car(config.boxNumberOutPlan)
    changebox.change_box()
    changebox.closeWindow()
    cls = driver.window_handles
    driver.switch_to.window(cls[0])









if __name__ == '__main__':
    pytest.main(['-vs','--alluredir','../allure-result'])
    #os.system('allure generate ../allure-result -o ../reports')