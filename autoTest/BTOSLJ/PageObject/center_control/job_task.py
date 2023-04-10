import allure
import pytest_check as check

from BTOSLJ.Config import config
from Base.basepage import BasePage
from BTOSLJ.Controls.BTOS_text import BtosText
from BTOSLJ.Controls.BTOS_table import BTOS_table


class JobTask(BasePage):
    '''
        当班作业任务
    '''
    def __init__(self, driver):
        super(JobTask, self).__init__(driver)
        self.textInput = BtosText(self.driver)
        self.table_work = BTOS_table(self.driver, 1)
        self.table_right = BTOS_table(self.driver, 6)
        self.table_left = BTOS_table(self.driver, 5)

    def search(self,input):
        self.textInput.select_by_label("工班", input['工班'])
        self.click('x', "//span[text()='检索 ']")

    # 新增舱单号
    @allure.step("理货员安排")
    def arrange_tallyman(self, input):
        self.table_work.select_row("船名航次", config.importNumber)
        self.click("id", "Tallyman")
        if self.elementExist('x', f"(//table[@class='vxe-table--body'])[5]//span[text()='{input['工号值']}']"):
            self.table_left.check("理货员编号", input['工号值'])
            self.left_click('x', "//i[@class='el-icon-arrow-right']")
            self.table_right.select_row("理货员编号", input['工号值'])
            self.left_click('x', "//span[text()='保存']")
            self.check_alert("保存成功")

    def check_table_task(self, input):
        rowid = self.table_work.select_row("船名航次", config.importNumber)
        check.equal(self.table_work.get_value_by_rowid(rowid, "作业类型"), "大船作业任务")
        check.equal(self.table_work.get_value_by_rowid(rowid, "舱口"), "01")
        check.equal(self.table_work.get_value_by_rowid(rowid, "作业区"), input["作业区"])
        check.equal(self.table_work.get_value_by_rowid(rowid, "作业工艺"), input["作业工艺"])
        check.equal(self.table_work.get_value_by_rowid(rowid, "操作过程"), input["操作过程"])
        check.equal(self.table_work.get_value_by_rowid(rowid, "货名"), input["货名"])
