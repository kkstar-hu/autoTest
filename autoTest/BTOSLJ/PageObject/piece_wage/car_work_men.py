import allure
import pytest_check as check

from BTOSLJ.Config import config
from Base.basepage import BasePage
from BTOSLJ.Controls.BTOS_text import BtosText
from BTOSLJ.Controls.BTOS_table import BTOS_table
from Commons.DateTime import DataTime


class CarWorkMen(BasePage):
    '''
       车驳库作业票-人事
    '''
    def __init__(self, driver):
        super(CarWorkMen, self).__init__(driver)
        self.textInput = BtosText(self.driver)
        self.table_input = BTOS_table(self.driver, 1)
        self.table_check = BTOS_table(self.driver, 2)
        self.table_people = BTOS_table(self.driver, 3)

    def search(self, input):
        self.textInput.select_by_label("工班", input['工班'])
        self.click('x', "//span[text()='检索 ']")
        self.waitloading()

    def edit(self, input):
        self.logger.info("车驳库场作业票-仓库-编辑")
        self.table_input.select_row("船名", config.importNumber)
        self.click("x", "//span[text()='编辑']")
        self.waitloading()
        self.table_people.input_by_row("定额编号", input["定额编号"])
        self.textInput.click("xpath", "//span[text()='保存']")
        self.check_alert(input["work_task_alert"])

    def check_table(self, input):
        self.table_input.select_row("船名", config.importNumber)
        check.equal(self.table_check.get_value("操作过程"), input["操作过程"])
        check.equal(self.table_check.get_value("货名"), input["货名"])
        check.equal(self.table_check.get_value("包装"), input["包装"])
        check.equal(self.table_check.get_value("货名"), input["货名"])
        check.equal(self.table_check.get_value("件数"), input["件数"])
        check.equal(self.table_check.get_value("吨位"), input["吨位"])

