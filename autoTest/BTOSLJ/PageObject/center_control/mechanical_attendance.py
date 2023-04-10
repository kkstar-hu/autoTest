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
        self.click("x", "//span[text()='安排机械']")
        self.waitloading()
        self.click("x", "//div[@role='treeitem']//span[text()='全选']")
        try:
            self.table_input.check("机械号", input['机械号'])
        except:
            pass
        self.left_click('x', "//span[text()='保存']")
        self.check_alert("保存成功")

    def check_table_task(self, input):
        check.equal(self.table_work.get_value("作业类型"), "大船作业任务")
        check.equal(self.table_work.get_value("舱口"), "01")
        check.equal(self.table_work.get_value("作业区"), input["作业区"])
        check.equal(self.table_work.get_value("工艺"), input["作业工艺"])
        check.equal(self.table_work.get_value("操作过程"), input["操作过程"])
        check.equal(self.table_work.get_value("货名"), input["货名"])
