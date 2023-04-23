from pytest_check import check

from BTOSLJ.Config import config
from Base.basepage import BasePage
from BTOSLJ.Controls.BTOS_text import BtosText
from BTOSLJ.Controls.BTOS_table import BTOS_table
global plan_number


class InCross(BasePage):
    """
    进门道口管理
    """
    def __init__(self, driver):
        super(InCross, self).__init__(driver)
        self.textInput = BtosText(self.driver)
        self.table_work = BTOS_table(self.driver, 1)

    def check(self):
        self.textInput.input_by_label("受理号", config.acceptNumber)
        self.textInput.select_by_label("车牌", "沪")
        self.textInput.input_by_placeholder("请输入车牌", "test10")
        self.click('x', "//span[text()='校验']")
        self.waitloading()
        self.click('x', "//span[text()='放行']")
        self.check_alert("放行成功")

