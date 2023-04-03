import time

import allure
import pytest_check as check
from selenium.webdriver import Keys
from Base.basepage import BasePage
from BTOSLJ.Controls.BTOS_text import BtosText
from BTOSLJ.Controls.BTOS_table import BTOS_table
from Commons.DateTime import DataTime
from Commons.RandomFunction import CommonGenerator


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
        self.click("x", "//div[@class='el-message-box__btns']//span[contains(text(),'确定')]")
        self.textInput.input_by_label("货名", "煤炭及制品")
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
        self.textInput.click("xpath", "(//span[text()='保存'])[1]")
        self.check_alert(input["alert"])

    def check_table_bill(self, input):
        self.rowid = self.table_bill.select_row("舱单号", self.billNumber)
        check.equal(self.table_bill.get_value_by_rowid(self.rowid, '来源港'), input["来源港"])
        check.equal(self.table_bill.get_value_by_rowid(self.rowid, '货代'), input["货代"])
        check.equal(self.table_bill.get_value_by_rowid(self.rowid, '货主'), input["货主"])
        check.equal(self.table_bill.get_value_by_rowid(self.rowid, '总件数'), input["件数"])
        check.equal(self.table_bill.get_value_by_rowid(self.rowid, '总重量'), input["重量"])
        check.equal(self.table_bill.get_value_by_rowid(self.rowid, '总体积'), input["体积"])
        check.equal(self.table_bill.get_value_by_rowid(self.rowid, '贸易条款'), input["贸易条款"])
        check.equal(self.table_bill.get_value_by_rowid(self.rowid, '备注'), input["备注"])

    def check_table_goods(self, input):
        self.rowid = self.table_goods.select_row("货名", "煤炭及制品")
        check.equal(self.table_goods.get_value_by_rowid(self.rowid, '唛头'), input["唛头"])
        check.equal(self.table_goods.get_value_by_rowid(self.rowid, '件数'), input["件数"])
        check.equal(self.table_goods.get_value_by_rowid(self.rowid, '重量'), input["重量"])
        check.equal(self.table_goods.get_value_by_rowid(self.rowid, '体积'), input["体积"])
        check.equal(self.table_goods.get_value_by_rowid(self.rowid, '包装'), input["包装"])




