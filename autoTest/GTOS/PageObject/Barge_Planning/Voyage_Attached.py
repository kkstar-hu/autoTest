import time
import pytest_check as check
from Base.basepage import BasePage
from GTOS.Controls.text import Gtos_text
from GTOS.Config import config
from GTOS.Controls.Gtos_table import Gtos_table

class Voyage_Attached(BasePage):
    """
    驳船策划--航次挂靠港
    """
    def input_values(self,input):
        """
        输入船名航次
        """
        self.logger.info('步骤1：选择船名航次')
        textInput = Gtos_text(self.driver)
        textInput.search_select_by_label('船名航次',input['船名航次2'])

    def Retrieval(self):
        """
        检索
        """
        self.logger.info('步骤2：点击检索')
        self.click('x',"(//span[text()='检索'])[1]")

    def Add(self):
        """
        新增航次挂靠港
        """
        self.logger.info('步骤3：新增挂靠港')
        self.click('x',"(//span[text()='新增'])[1]")
        textInput = Gtos_text(self.driver)
        # textInput.search_select_by_label('港口代码','CNWHA')
        # textInput.input_noclear_placeholder_click('请选择','CNWHA')
        textInput.click('x',"(//input[@placeholder='请选择'])[1]")
        textInput.click('x',"//span[text()='CNWHA']")
        # textInput.input_no_clear('x',"(//input[@placeholder='请选择'])[1]",'CNWHA')
        # textInput.click('x',"(//span[text()='CNWHA'])[1]")
        textInput.click('x',"//span[text()='保 存']")
        self.check_alert('')

    def process(self,input):
        """
        流程
        """
        self.input_values(input)
        self.Retrieval()
        self.close_alert('未找到相关航次挂靠港数据')
        self.Add()