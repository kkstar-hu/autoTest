import time
import allure
import pytest_check as check
from selenium.webdriver import Keys
from Base.basepage import BasePage
from BTOSLJ.Controls.BTOS_text import BtosText
from BTOSLJ.Controls.BTOS_table import BTOS_table
from Commons.RandomFunction import CommonGenerator


class ImStoreBill(BasePage):
    '''
        内贸进口仓单管理
    '''
    def __init__(self, driver):
        super(ImStoreBill, self).__init__(driver)
        self.textInput = BtosText(self.driver)
        self.table_bill = BTOS_table(self.driver, 1)
        self.table_goods = BTOS_table(self.driver, 2)
        self.rowid = None
        self.billNumber = CommonGenerator.generate_verify_code(4)

    def search(self, number):
        self.textInput.select_by_label_ship("船名航次", number)
        self.click('x', "//span[text()='检索 ']")

    # 新增舱单号
    @allure.step("新增舱单号")
    def add_bill(self, number, input):
        self.logger.info("内贸进口舱单管理-新增舱单号")
        self.textInput.select_by_label_ship("船名航次", number)
        self.waitloading()
        self.click("x", "//div[@id='add']/span[text()='新增']")
        self.textInput.input_by_label("舱单号", self.billNumber)
        self.textInput.select_by_label("货代", input["货代"])
        self.textInput.select_by_label_time("货主", input["货主"])
        self.textInput.select_by_label("来源港", input["来源港"])
        self.textInput.select_by_label("贸易条款", input["贸易条款"])
        self.textInput.select_by_label("舱单类型", input["舱单类型"])
        self.textInput.input_by_label("备注", input["备注"])
        self.click("x", "//div[@id='add']/span[text()='新增货物']")
        self.textInput.input_by_label("唛头", input['唛头'])
        self.textInput.input_by_label("货名", "煤炭及制品")
        time.sleep(1)
        self.get_element("x", "//label[contains(text(),'货名')]//following-sibling::div//input").send_keys(Keys.ENTER)
        self.textInput.select_by_label("包装", input['包装'])
        self.click("x", "//label[contains(text(),'包装')]")
        self.textInput.input_by_label("件数", input['件数'])
        self.textInput.input_by_label("重量", input['重量'])
        self.textInput.input_by_label("体积", input['体积'])
        self.textInput.click("xpath", "(//span[text()='保存'])[2]")
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
        self.rowid = self.table_goods.select_row("货名", input["货名"])
        time.sleep(1)
        check.equal(self.table_goods.get_value_by_rowid(self.rowid, '唛头'), input["唛头"])
        check.equal(self.table_goods.get_value_by_rowid(self.rowid, '件数'), input["件数"])
        check.equal(self.table_goods.get_value_by_rowid(self.rowid, '重量'), input["重量"])
        check.equal(self.table_goods.get_value_by_rowid(self.rowid, '体积'), input["体积"])
        check.equal(self.table_goods.get_value_by_rowid(self.rowid, '包装'), input["包装"])




