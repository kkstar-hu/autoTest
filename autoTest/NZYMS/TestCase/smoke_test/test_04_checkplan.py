import os
import allure
from Commons.Controls.tag import Tag
from Commons.menu import Menu
from Commons.yamlread import read_yaml
from NZYMS.config import config
from NZYMS.PageObject.BoxManagement.checkPlan import Check_Plan
import pytest as pytest
from NZYMS.PageObject.BoxManagement.inputCheckInfo import Input_Check_Info
from NZYMS.PageObject.PayManagement.Settlement_charge import Settlement_Charge

@allure.story('4.查验流程')
@allure.title('1.添加查验计划')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(),'04_checkboxprocess','checkPlan.yaml')))
def testCheckPlan(driver,input):
    menu = Menu(driver)
    menu.select_level_Menu("箱务管理,查验计划")
    checkplan=Check_Plan(driver)
    checkplan.addcheckPlan(input)


@allure.story('4.查验流程')
@allure.title('2.添加查验箱')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(),'04_checkboxprocess','checkPlan.yaml')))
def testAddPlanBox(driver, input):
    checkplan = Check_Plan(driver)
    checkplan.addWorkOrder(input,config.boxNumber)
    #checkplan.clickExcute(1)
    Tag(driver).closeTag("查验计划")


@allure.story('4.查验流程')
@allure.title('3.查验过程录入')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(),'04_checkboxprocess','inputCheckInfo.yaml')))
def testeditcheckinfo(driver,input):
    menu = Menu(driver)
    menu.select_level_Menu("箱务管理,查验过程录入")
    checkinfo=Input_Check_Info(driver)
    checkinfo.editPlan(input,config.boxNumber)
    Tag(driver).closeTag("查验过程录入")


@allure.story('4.查验流程')
@allure.title('4.查验结算收费')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(),'04_checkboxprocess','checkPlan.yaml')))
def testchargepay(driver,input):
    menu = Menu(driver)
    menu.select_level_Menu("费收管理,费用管理,结算收费")
    charge = Settlement_Charge(driver)
    charge.search(config.boxNumber, "15/查验计划")
    charge.check_check_plan_information(input)
    charge.configuration()
    charge.check_checkbox(input)
    charge.pay(input)
    driver.refresh()



