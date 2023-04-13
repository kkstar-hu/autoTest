import time

import allure
import pytest_check as check
from selenium.webdriver import Keys
from Base.basepage import BasePage
from BTOSLJ.Controls.BTOS_text import BtosText
from BTOSLJ.Controls.BTOS_table import BTOS_table
from Commons.DateTime import DataTime

global plan_number


class BigShipWorkPlan(BasePage):
    '''
        大船作业计划
    '''
    def __init__(self, driver):
        super(BigShipWorkPlan, self).__init__(driver)
        self.textInput = BtosText(self.driver)
        self.table_work = BTOS_table(self.driver, 1)
        self.rowid = None

    def search(self, number):
        self.textInput.select_by_label_ship("船名航次", number)
        self.click('x', "(//span[text()='检索 '])[2]")

    # 新增舱单号
    @allure.step("新增大船计划-安排计划")
    def add_plan(self, number, input):
        self.logger.info("大船计划管理：新增大船计划-安排计划")
        leaveDay = DataTime.Get_Date_X_Number_Of_Days(-1)
        leaveTime = leaveDay + " 00:00:00"
        self.textInput.input_by_label("计划时间", leaveTime)
        self.waitloading()
        self.click("x", "//div[@id='add']/span[text()='新增']")
        self.search(number)
        time.sleep(1)
        self.click("x", "(//div[@class='toscom-buttongroup']//span[text()='安排计划'])[2]")
        self.waitloading()
        self.get_element("x", "//label[contains(text(),'货名')]//following-sibling::div//input").send_keys(Keys.ENTER)
        self.textInput.input_by_label("计划吨位", input["计划吨位"])
        self.textInput.input_by_label("昼夜剩余吨位", input["昼夜剩余吨位"])
        self.textInput.input_by_label("计划备注", input["计划备注"])
        self.textInput.input_by_number("作业路数", input["作业路数"], 1)
        self.textInput.select_by_index("操作过程", input['操作过程'], 4)
        self.textInput.select_by_index("作业工艺", input['作业工艺'], 4)
        self.click("x", "//label[contains(text(),'计划备注')]//following-sibling::div//input")
        self.textInput.select_by_index("队列", input['队列'], 2)
        self.textInput.input_by_number("人数", input['人数'], 1)
        self.textInput.select_by_index("类型", input['类型'], 2)
        self.textInput.input_by_number("数量", input['数量'], 1)
        self.textInput.click("xpath", "(//span[text()='保存并关闭'])[1]")
        self.check_alert(input["alert"])

    def check_table_plan(self, input):
        check.equal(self.table_work.get_value("装/卸"), input["装/卸"])
        check.equal(self.table_work.get_value("作业区"), input["作业区"])
        check.equal(self.table_work.get_value("贸易类型"), input["贸易类型"])
        check.equal(self.table_work.get_value("操作过程"), input["操作过程"])
        check.equal(self.table_work.get_value("货名"), input["货名"])
        check.equal(self.table_work.get_value("计划备注"), input["计划备注"])






