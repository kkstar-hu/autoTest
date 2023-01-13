import time
import pytest_check as check
from Base.basepage import BasePage
from GTOS.Controls.text import Gtos_text
from GTOS.Config import config
from GTOS.Controls.Gtos_table import Gtos_table


class Bridge_Crane_Distribution(BasePage):
    """
    驳船策划--桥吊资源分配
    """
    def input_values(self,input):
        """
        输入船名航次
        """
        self.logger.info('步骤1：选择船名航次')
        textInput = Gtos_text(self.driver)
        # textInput.search_select_by_label('船名航次',input['船名航次1'])
        textInput.search_select_by_label('船名航次',config.importNumber)

    def Retrieval(self):
        """
        检索
        """
        self.logger.info('步骤2：点击检索')
        self.click('x',"(//span[text()='检索'])[2]")

    def get_values(self):
        """
        勾选内容，分配桥吊
        """
        self.logger.info('步骤3：勾选内容，分配桥吊')
        tablecheck = Gtos_table(self.driver,3)
        tablecheck.tick_off_box(1)
        tablecheck.click('x',"//span[text()='安排桥吊资源']")
        tablecheck.click('x',"//label//span[text()='B109']")
        tablecheck.click('x',"//span[text()='保 存']")
        self.check_alert('')

    def process(self,input):
        """
        流程
        """
        self.input_values(input)
        self.Retrieval()
        self.get_values()
