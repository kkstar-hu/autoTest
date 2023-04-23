import time

import allure
import pytest_check as check
from BTOSLJ.Config import config
from Base.basepage import BasePage
from BTOSLJ.Controls.BTOS_text import BtosText
from BTOSLJ.Controls.BTOS_table import BTOS_table


class DomesticTradeAcceptGoods(BasePage):
    '''
        内贸提货受理
    '''
    def __init__(self, driver):
        super(DomesticTradeAcceptGoods, self).__init__(driver)
        self.textInput = BtosText(self.driver)
        self.table_bill = BTOS_table(self.driver, 7)
        self.table_good = BTOS_table(self.driver, 9)
        self.table_accept = BTOS_table(self.driver, 1)

    def search(self,input):
        self.textInput.select_by_label_ship("船名航次", config.importNumber)
        self.textInput.select_by_label("操作过程", input["操作过程"])
        self.click('x', "(//span[text()='检索 '])[2]")

    # 新增受理信息
    @allure.step("新增受理信息")
    def add_acceptance_information(self, input):
        self.logger.info("新增受理信息")
        self.click("id", "add")
        self.search(input)
        self.waitloading()
        colid = self.get_attribute_info("xpath", f"(//table[@class='vxe-table--header'])[7]//thead/tr/th//span[text()='操作']//parent::div//parent::th",
                                        "colid")
        rowid = self.table_bill.select_row("舱单号", config.billNumber)
        time.sleep(0.5)
        self.click("x", f"(//tr[@rowid='{rowid}']/td[@colid='{colid}']//div[@class='operate']//span[text()='导入场地货'])[2]")
        time.sleep(0.5)
        self.textInput.click("xpath", "//span[text()='保存']")
        self.check_alert(None)

    def check_table_bill(self, input):
        check.equal(self.table_good.get_value("货名"), input["货名"])
        check.equal(self.table_good.get_value("唛头"), input["唛头"])
        check.equal(self.table_good.get_value("件数"), input["件数"])
        #check.equal(self.table_good.get_value("体积"), input["体积"])
        check.equal(self.table_good.get_value("重量"), input["重量"])
        check.equal(self.table_good.get_value("包装"), input["包装"])

    def click_next_button(self):
        self.click("xpath", "//span[text()='下一步']")

    @allure.step("新增受理信息")
    def deal_acceptance_information(self, input):
        self.logger.info("内贸提货受理")
        self.textInput.select_by_label("运输公司", input["运输公司"])
        self.textInput.input_by_label("运输公司电话", input["运输公司电话"])
        self.textInput.click("xpath", "//span[text()='保存']")
        self.check_alert(input['alert'])
        rowid = self.table_accept.select_row("舱单号", config.billNumber)
        config.acceptNumber = self.table_accept.get_value_by_rowid(rowid, "受理号")
        self.logger.info("受理号"+config.acceptNumber)