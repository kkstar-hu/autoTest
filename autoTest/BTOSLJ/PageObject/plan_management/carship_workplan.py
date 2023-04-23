import time

import allure
import pytest_check as check
from selenium.webdriver import Keys

from BTOSLJ.Config import config
from Base.basepage import BasePage
from BTOSLJ.Controls.BTOS_text import BtosText
from BTOSLJ.Controls.BTOS_table import BTOS_table
from Commons.DateTime import DataTime

global plan_number


class CarShipWorkPlan(BasePage):
    '''
        车驳作业计划
    '''
    def __init__(self, driver):
        super(CarShipWorkPlan, self).__init__(driver)
        self.textInput = BtosText(self.driver)
        self.table_work = BTOS_table(self.driver, 1)
        self.table_accept = BTOS_table(self.driver, 3)

    def search(self):
        workDay = DataTime.Get_Date_X_Number_Of_Days(-1)
        workTime = workDay + " 00:00:00"
        self.textInput.input_by_label("计划时间", workTime)
        self.click('x', "//span[text()='检索 ']")
        self.waitloading()

    # 新增舱单号
    @allure.step("车驳作业计划-新增")
    def add_plan(self, input):
        self.logger.info("大船计划管理：新增大船计划-安排计划")
        self.click("x", "//div[@id='add']/span[text()='新增']")
        time.sleep(1)
        colid = self.get_attribute_info("xpath",
                                        f"(//table[@class='vxe-table--header'])[3]//thead/tr/th//span[text()='操作']//parent::div//parent::th",
                                        "colid")
        rowid = self.table_accept.select_row("船名航次", config.importNumber)
        time.sleep(0.5)
        self.click("x", f"(//tr[@rowid='{rowid}']/td[@colid='{colid}']//div[@class='operate']//span[text()='安排计划'])[2]")
        self.waitloading()
        self.textInput.input_by_number("作业路数", input["作业路数"], 1)
        self.textInput.input_by_label("人数", input['人数'])
        self.textInput.select_by_label("装卸队", input['装卸队'])
        self.textInput.click("xpath", "(//span[text()='保存并关闭'])[1]")
        self.check_alert(input["alert"])

    def check_table_plan(self, input):
        check.equal(self.table_work.get_value("装/卸"), input["装/卸"])
        check.equal(self.table_work.get_value("作业区"), input["作业区"])
        check.equal(self.table_work.get_value("贸易类型"), input["贸易类型"])
        check.equal(self.table_work.get_value("操作过程"), input["操作过程"])
        check.equal(self.table_work.get_value("货名"), input["货名"])
        check.equal(self.table_work.get_value("计划备注"), input["计划备注"])






