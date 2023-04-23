import time

import allure
import pytest_check as check

from BTOSLJ.Config import config
from Base.basepage import BasePage
from BTOSLJ.Controls.BTOS_text import BtosText
from BTOSLJ.Controls.BTOS_table import BTOS_table
from Commons.DateTime import DataTime


class CarWorkStore(BasePage):
    '''
        车驳库作业票-仓库
    '''
    def __init__(self, driver):
        super(CarWorkStore, self).__init__(driver)
        self.textInput = BtosText(self.driver)
        self.table_input = BTOS_table(self.driver, 1)
        self.table_check = BTOS_table(self.driver, 2)

    def search(self, input):
        self.textInput.select_by_label("工班", input['工班'])
        self.click('x', "//span[text()='检索 ']")
        self.waitloading()

    def generate(self):
        self.logger.info("车驳库场作业票-仓库-生成")
        self.table_input.select_row("船名", config.importNumber)
        time.sleep(1)
        self.waitloading()
        self.click("x", "//span[text()='生成']")
        self.waitloading()
        self.check_alert("生成成功!")

    def add_foreman(self,input):
        self.logger.info("车驳库场作业票-仓库-新增装卸队")
        self.table_input.select_row("船名", config.importNumber)
        self.click("x", "//span[text()='新增']")
        self.waitloading()
        self.textInput.select_by_label("货名", input["装卸队货名"])
        self.textInput.select_by_label("包装", input["包装"])
        self.textInput.input_by_label("件数", input["件数"])
        self.textInput.input_by_label("吨位", input["吨位"])
        self.textInput.select_by_label("操作过程", input["操作过程"])
        self.textInput.click("xpath", "//span[text()='保存']")
        self.check_alert(input["alert"])

    def audit(self):
        self.logger.info("装卸船作业票中控-审核")
        rowid = self.table_input.select_row("船名", config.importNumber)
        self.click("xpath", f"(//table[@class='vxe-table--body'])[1]//tr[@rowid='" + rowid + "']//span[text()='审核']")

    def check_table(self, input):
        self.table_input.select_row("船名", config.importNumber)
        check.equal(self.table_check.get_value("操作过程"), input["操作过程"])
        check.equal(self.table_check.get_value("货名"), input["货名"])
        check.equal(self.table_check.get_value("包装"), input["包装"])
        check.equal(self.table_check.get_value("货名"), input["货名"])
        check.equal(self.table_check.get_value("件数"), input["件数"])
        check.equal(self.table_check.get_value("吨位"), input["吨位"])

