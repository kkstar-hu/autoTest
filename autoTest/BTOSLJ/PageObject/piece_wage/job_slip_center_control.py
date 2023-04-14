import allure
import pytest_check as check

from BTOSLJ.Config import config
from Base.basepage import BasePage
from BTOSLJ.Controls.BTOS_text import BtosText
from BTOSLJ.Controls.BTOS_table import BTOS_table
from Commons.DateTime import DataTime


class JobSlipControl(BasePage):
    '''
        装卸船作业票
    '''
    def __init__(self, driver):
        super(JobSlipControl, self).__init__(driver)
        self.textInput = BtosText(self.driver)
        self.table_input = BTOS_table(self.driver, 1)
        self.table_check = BTOS_table(self.driver, 2)

    def search(self, input):
        self.textInput.select_by_label("工班", input['工班'])
        self.click('x', "//span[text()='检索 ']")
        self.waitloading()

    #  一键生成
    @allure.step("装卸船作业票中控-一键生成")
    def generate(self):
        self.logger.info("装卸船作业票中控-一键生成")
        self.table_input.select_row("船名", config.importNumber)
        self.click("x", "//span[text()='一键生成']")
        self.waitloading()
        self.check_alert("生成成功!")

    @allure.step("装卸船作业票中控-审核")
    def audit(self):
        self.logger.info("装卸船作业票中控-审核")
        rowid=self.table_input.select_row("船名", config.importNumber)
        self.click("xpath",
                   f"(//table[@class='vxe-table--body'])[1]//tr[@rowid='" + rowid + "']//span[text()='审核']")

    def check_table(self, input):
        check.equal(self.table_check.get_value("操作过程"), input["操作过程"])
        check.equal(self.table_check.get_value("货名"), input["货名"])
        check.equal(self.table_check.get_value("包装"), input["包装"])
        check.equal(self.table_check.get_value("货名"), input["货名"])
        check.equal(self.table_check.get_value("件数"), input["件数"])
        check.equal(self.table_check.get_value("吨位"), input["重量"])
        check.equal(self.table_check.get_value("起点"), input["机械号"])
