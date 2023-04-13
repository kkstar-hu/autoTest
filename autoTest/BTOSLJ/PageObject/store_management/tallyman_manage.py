import time

from BTOSLJ.Controls.BTOS_table import BTOS_table
from BTOSLJ.Controls.BTOS_text import BtosText
from Base.basepage import BasePage
from Commons.DateTime import DataTime


class Tallyman(BasePage):
    def __init__(self, driver):
        super(Tallyman, self).__init__(driver)
        self.textInput = BtosText(self.driver)
        self.table_left = BTOS_table(self.driver, 1)
        self.table_right = BTOS_table(self.driver, 2)

    def select_people(self, input: dict):
        self.textInput.select_by_label("部门", input["部门"])
        self.textInput.select_by_label("工班", input["工班"])
        self.left_click('x', "//span[text()=' 检索 ']")
        time.sleep(0.5)
        if self.elementExist('x', f"(//table[@class='vxe-table--body'])[1]//span[text()='{input['工号值']}']"):
            self.table_left.check("工号", input['工号值'])
            self.left_click('x', "//i[@class='el-icon-arrow-right']")
            self.table_right.select_row("工号", input['工号值'])
            self.click('x', "//span[text()=' 保存 ']")
            self.check_alert(input['work_task_alert'])
