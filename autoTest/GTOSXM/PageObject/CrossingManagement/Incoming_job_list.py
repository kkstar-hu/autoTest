import pytest_check as check
from Base.basepage import BasePage
from GTOSXM.Controls.text import Gtos_text
from GTOSXM.Config import configinterface
from GTOSXM.Controls.Gtos_table import Gtos_table


class Incoming_job_list(BasePage):
    """
    进场作业列表
    """

    def input_values(self):
        """
        输入查询内容
        """
        self.logger.info('进场作业列表：输入数据')
        textInput = Gtos_text(self.driver)
        textInput.input_by_label("箱号", configinterface.boxNumber)

    def check_first(self):
        """
        第一次查验
        """
        self.click('xpath', "//span[text()='检索']")
        tablecheck = Gtos_table(self.driver)
        check.equal(tablecheck.get_value('作业状态'), '允许作业')

    def check_second(self):
        """
        第二次查验
        """
        self.click('xpath', "//span[text()='检索']")
        tablecheck = Gtos_table(self.driver)
        check.equal(tablecheck.get_value('作业状态'), '完成')
