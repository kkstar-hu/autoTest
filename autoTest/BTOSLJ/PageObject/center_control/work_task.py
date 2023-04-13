import allure
import pytest_check as check

from BTOSLJ.Config import config
from Base.basepage import BasePage
from BTOSLJ.Controls.BTOS_text import BtosText
from BTOSLJ.Controls.BTOS_table import BTOS_table
from Commons.DateTime import DataTime


class WorkTask(BasePage):
    '''
        当班作业任务
    '''
    def __init__(self, driver):
        super(WorkTask, self).__init__(driver)
        self.textInput = BtosText(self.driver)
        self.table_work = BTOS_table(self.driver, 1)
        self.table_arrange = BTOS_table(self.driver, 3)

    def search(self, input):
        self.textInput.select_by_label("工班", input['工班'])
        self.click('x', "//span[text()='检索 ']")

    # 新增舱单号
    @allure.step("当班作业任务-昼夜计划导入")
    def add_plan(self, input):
        self.logger.info("当班作业任务：昼夜计划导入")
        self.textInput.select_by_label("工班", input["工班"])
        self.waitloading()
        self.click("id", "add_1")
        self.waitloading()
        colid = self.get_attribute_info("xpath", f"(//table[@class='vxe-table--header'])[3]//thead/tr/th//span[text()='操作']//parent::div//parent::th",
                                        "colid")
        rowid=self.table_arrange.select_row("船名航次", config.importNumber)
        self.click("x", f"(//tr[@rowid='{rowid}']/td[@colid='{colid}']//div[@class='operate']//span[text()='安排作业路'])[2]")
        self.click("xpath", "//label[contains(text(),'舱口')]//following-sibling::div//input")
        self.waitloading()
        self.click("xpath", "//div[@class='nz-flex-col']//div[text()='01']")
        self.textInput.input_by_label("任务吨位", input["任务吨位"])
        self.textInput.select_by_index("作业工艺", input['作业工艺'], 0)
        self.textInput.select_by_index("作业节点", input['作业节点'], 0)
        self.textInput.select_by_index("作业节点", input['作业节点'], 2)
        self.textInput.click("xpath", "(//span[text()='保存'])[1]")
        self.check_alert(input["work_task_alert"])
        self.click("xpath", "//button[@aria-label='close 作业任务']")
        self.click("xpath", "//button[@aria-label='close 昼夜计划导入']")

    def check_table_task(self, input):
        check.equal(self.table_work.get_value("作业类型"), "大船作业任务")
        check.equal(self.table_work.get_value("舱口"), "01")
        check.equal(self.table_work.get_value("作业区"), input["作业区"])
        check.equal(self.table_work.get_value("工艺"), input["作业工艺"])
        check.equal(self.table_work.get_value("操作过程"), input["操作过程"])
        check.equal(self.table_work.get_value("货名"), input["货名"])
