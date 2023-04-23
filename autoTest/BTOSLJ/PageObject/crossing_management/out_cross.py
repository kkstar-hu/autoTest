from pytest_check import check

from BTOSLJ.Config import config
from Base.basepage import BasePage
from BTOSLJ.Controls.BTOS_text import BtosText
from BTOSLJ.Controls.BTOS_table import BTOS_table
global plan_number


class OutCross(BasePage):
    """
    出门道口管理
    """
    def __init__(self, driver):
        super(OutCross, self).__init__(driver)
        self.textInput = BtosText(self.driver)
        self.table_work = BTOS_table(self.driver, 1)

    def search(self):
        self.click('x', "//span[text()='检索 ']")
        self.waitloading()

    def out(self,input):
        rowid = self.table_work.select_row("车牌", "沪TEST10")
        self.waitloading()
        self.left_click("xpath", f"(//table[@class='vxe-table--body'])[1]//tr[@rowid='" + rowid + "']//span[text()='放行']")
        self.textInput.select_by_label("道口", input["道口"])
        self.click('x', "//div[@class='footer']//span[text()='放行']")

