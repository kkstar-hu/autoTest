import time

import allure
import pytest_check as check

from BTOSLJ.Config import config
from Base.basepage import BasePage
from BTOSLJ.Controls.BTOS_text import BtosText
from BTOSLJ.Controls.BTOS_table import BTOS_table
from Commons.DateTime import DataTime


class WorkTaskReport(BasePage):
    '''
        作业任务汇报
    '''
    def __init__(self, driver):
        super(WorkTaskReport, self).__init__(driver)
        self.textInput = BtosText(self.driver)
        self.table_cargo_manifest = BTOS_table(self.driver, 10)
        self.table_input = BTOS_table(self.driver, 11)
        self.table_task = BTOS_table(self.driver, 1)
        self.table_check = BTOS_table(self.driver, 3)

    def search(self, input):
        self.textInput.select_by_label("工班", input['工班'])
        self.click('x', "//span[text()='检索 ']")
        self.waitloading()

    def select_row_ship(self):
        self.table_task.select_row("船名航次", config.importNumber)

    def select_row_accept_number(self):
        self.table_task.select_row("受理号", config.acceptNumber)

    #  理货汇报
    @allure.step("作业任务汇报-理货汇报")
    def report(self, input):
        self.logger.info("作业任务汇报：理货汇报")
        self.click("x", "//span[text()='理货汇报']")
        self.table_cargo_manifest.select_row("舱单", config.billNumber)
        self.waitloading()
        self.textInput.select_by_label("理货员", input["理货员"])
        self.textInput.select_by_label("指导配置", input["指导配置"])
        self.textInput.select_by_label("实际工班", input["实际工班"])
        self.table_input.input_by_row("货位", input["货位"])
        self.click("xpath", f"//div[@class='el-scrollbar']//span[contains(text(),'{input['货位']}')]")
        self.table_input.input_select_by_row("操作过程", input["操作过程"])
        self.textInput.select_by_label("理货配置", input["理货配置"])
        self.table_input.input_by_row("重量(吨)", input["重量"])
        self.table_input.input_by_row("件数", input["件数"])
        if self.hasInput(input, "车驳号"):
            self.textInput.select_by_label("车驳号", input["车驳号"])
        self.textInput.click("xpath", "(//span[text()='保存并关闭'])[1]")
        self.check_alert(input["work_task_alert"])

    def audit_task(self):
        self.logger.info("当班作业任务-审核")
        rowid = self.table_task.select_row("受理号", config.acceptNumber)
        time.sleep(1)
        self.click("xpath", f"(//table[@class='vxe-table--body'])[2]//tr[@rowid='" + rowid + "']//span[text()='审核']")
        time.sleep(1)
        self.click("x", "//span[text()='保存']")

    def audit_report(self):
        self.logger.info("理货汇报-审核")
        self.table_task.select_row("受理号", config.acceptNumber)
        time.sleep(1)
        rowid = self.table_check.select_row("受理号", config.acceptNumber)
        time.sleep(2)
        self.click("xpath", f"(//table[@class='vxe-table--body'])[4]//tr[@rowid='" + rowid + "']//span[text()='审核']")
        self.check_alert("审核成功")

    def check_table_task(self, input):
        check.equal(self.table_check.get_value("作业方式"), input['作业方式'])
        if self.hasInput(input, "舱口"):
            check.equal(self.table_check.get_value("舱口"), "01")
        check.equal(self.table_check.get_value("工班"), input["工班"])
        check.equal(self.table_check.get_value("舱单"), str(config.billNumber))
        check.equal(self.table_check.get_value("操作过程"), input["操作过程"])
        check.equal(self.table_check.get_value("货名"), input["货名"])
        check.equal(self.table_check.get_value("唛头"), input["唛头"])
        check.equal(self.table_check.get_value("货主"), input["货主"])
        check.equal(self.table_check.get_value("包装"), input["包装"])
        check.equal(self.table_check.get_value("货代"), input["货代"])
        check.equal(self.table_check.get_value("货名"), input["货名"])
        check.is_in(input["货位"],self.table_check.get_value("货位"))
        check.equal(self.table_check.get_value("件数"), input["件数"])
        check.equal(self.table_check.get_value("重量"), input["重量"])