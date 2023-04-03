from BTOSLJ.Controls.BTOS_table import BTOS_table
from BTOSLJ.Controls.BTOS_text import BtosText
from Base.basepage import BasePage
from Commons.DateTime import DataTime


class Tallyman(BasePage):
    def Out_For_Work(self, input: dict):
        self.textInput = BtosText(self.driver)
        self.tableInput = BTOS_table(self.driver)
        self.work_date = DataTime.Get_Current_Date()
        self.textInput.select_by_label("部门", input["部门"])
        self.textInput.input_by_label("工作日期", self.work_date)
        self.textInput.select_by_label("工班", input["工班"])
        self.left_click('x', "//span[text()=' 检索 ']")
        self.tableInput.check("工号", input['工号值'])
        self.left_click('x', "//i[@class='el-icon-arrow-right']")
        self.left_click('x', "//span[text()=' 保存 ']")
        self.check_alert("保存成功")