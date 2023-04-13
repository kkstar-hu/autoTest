import allure
import pytest_check as check
from BTOSLJ.Config import config
from Base.basepage import BasePage
from BTOSLJ.Controls.BTOS_text import BtosText
from BTOSLJ.Controls.BTOS_table import BTOS_table


class Ship_Leave_Stop(BasePage):
    '''
        大船靠离泊管理
    '''
    def __init__(self, driver):
        super(Ship_Leave_Stop, self).__init__(driver)
        self.textInput = BtosText(self.driver)
        self.table_check = BTOS_table(self.driver, 1)

    def search(self):
        self.textInput.search_select_by_label("船名", config.mydata.vsl_cnname)
        self.click('x', "//span[text()='检索 ']")
        self.waitloading()

    @allure.step("大船靠离泊-靠泊")
    def berthing_by(self):
        self.logger.info("大船靠离泊：靠泊")
        rowid = self.table_check.select_row("进口航次", config.importNumber)
        check.equal(self.table_check.get_value_by_rowid(rowid, "靠泊状态 "), "未靠")
        check.equal(self.table_check.get_value_by_rowid(rowid, "船期状态"), "确报")
        self.click("xpath",
                   f"(//table[@class='vxe-table--body'])[1]//tr[@rowid='" + rowid + "']//div[@id='berthingBy']")
        self.waitloading()
        self.left_click('x', "//span[text()='保存']")
        self.check_alert("靠泊成功")
        self.waitloading()
        rowid = self.table_check.select_row("进口航次", config.importNumber)
        check.equal(self.table_check.get_value_by_rowid(rowid, "靠泊状态 "), "已靠")
        check.equal(self.table_check.get_value_by_rowid(rowid, "船期状态"), "在港")


