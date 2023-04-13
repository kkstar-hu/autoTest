import allure
import pytest_check as check
from BTOSLJ.Config import config
from Base.basepage import BasePage
from BTOSLJ.Controls.BTOS_text import BtosText
from BTOSLJ.Controls.BTOS_table import BTOS_table


class MechanicalAttendance(BasePage):
    '''
        机械出勤
    '''
    def __init__(self, driver):
        super(MechanicalAttendance, self).__init__(driver)
        self.textInput = BtosText(self.driver)
        self.table_input = BTOS_table(self.driver, 2)
        self.table_check = BTOS_table(self.driver, 1)

    def search(self, input):
        self.textInput.select_by_label("工班", input['工班'])
        self.click('x', "//span[text()='检索 ']")
        self.waitloading()

    # 安排机械
    @allure.step("机械出勤-安排机械")
    def arrange_mechanical(self, input):
        self.logger.info("机械出勤：安排机械")
        if not self.table_check.hasValue("机械号", input['机械号']):
            self.click("x", "//span[text()='安排机械']")
            self.waitloading()
            self.click("x", "//div[@role='treeitem']//span[text()='全选']")
            self.table_input.check("机械号", input['机械号'])
            self.left_click('x', "//span[text()='保存']")
            self.check_alert("保存成功")

    @allure.step("机械出勤-安排司机")
    def arrange_driver(self, input):
        self.logger.info("机械出勤：安排司机")
        self.click("x", "//span[text()='安排司机']")
        self.waitloading()
        self.click("x", "//div[@role='treeitem']//span[text()='机械运行部']")
        self.table_input.check("工号", input['司机工号'])
        self.waitloading()
        self.click('x', "//span[text()='保存']")
        self.check_alert("保存成功")

    def check_table(self, input):
        rowid = self.table_check.select_row("机械号", input["机械号"])
        check.equal(self.table_check.get_value_by_rowid(rowid, "部门"), input["出勤部门"])
        check.equal(self.table_check.get_value_by_rowid(rowid, "机械类型"), input["机械类型"])
        check.equal(self.table_check.get_value_by_rowid(rowid, "状态"), "启用")
        check.equal(self.table_check.get_value_by_rowid(rowid, "已安排司机"), input['司机'])
