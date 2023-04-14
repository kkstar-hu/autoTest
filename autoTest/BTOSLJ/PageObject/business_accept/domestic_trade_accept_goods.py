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
        self.table_bill = BTOS_table(self.driver, 8)
        self.table_good = BTOS_table(self.driver, 9)

    def search(self):
        self.textInput.select_by_label_ship("船名航次", config.importNumber)
        self.textInput.select_by_label("船名航次", input['操作过程'])
        self.click('x', "(//span[text()='检索 '])[2]")

    # 新增受理信息
    @allure.step("新增受理信息")
    def add_acceptance_information(self, input):
        self.logger.info("新增受理信息")
        self.click("id", "add")
        self.search()
        self.waitloading()
        colid = self.get_attribute_info("xpath", f"(//table[@class='vxe-table--header'])[1]//thead/tr/th//span[text()='操作']//parent::div//parent::th",
                                        "colid")
        rowid=self.table_bill.select_row("舱单号", config.billNumber)

        self.click("x", f"//tr[@rowid='{rowid}']/td[@colid='{colid}']//div[@class='operate']//span[text()='导入场地货']")
        self.textInput.click("xpath", "(//span[text()='保存'])[4]")
        self.check_alert(input["alert"])

    def check_table_bill(self, input):
        check.equal(self.table_bill.get_value("货名"), input["货名"])
        check.equal(self.table_bill.get_value("唛头"), input["唛头"])
        check.equal(self.table_bill.get_value("货主"), input["货主"])
        check.equal(self.table_bill.get_value("货代"), input["货代"])
        check.equal(self.table_bill.get_value("货名"), input["货名"])
        check.equal(self.table_bill.get_value("场地剩余件数"), input["场地剩余件数"])
        check.equal(self.table_bill.get_value("场地剩数重量"), input["场地剩数重量"])