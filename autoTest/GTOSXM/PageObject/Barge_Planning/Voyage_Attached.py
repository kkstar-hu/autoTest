import time
import pytest_check as check
from Base.basepage import BasePage
from GTOSXM.Controls.text import Gtos_text
from GTOSXM.Config import config
from GTOS.Controls.Gtos_table import Gtos_table

class Voyage_Attached(BasePage):
    """
    驳船策划--航次挂靠港
    """
    def input_values(self):
        """
        输入船名航次
        """
        self.logger.info('航次挂靠港-选择船名航次'+config.outportNumber)
        textInput = Gtos_text(self.driver)
        textInput.search_select_by_label('船名航次',config.outportNumber)

    def Retrieval(self):
        """
        检索
        """
        self.click('x',"(//span[text()='检索'])[1]")

    def Add(self):
        """
        新增航次挂靠港
        """
        self.logger.info('航次挂靠港-新增挂靠港ARENS')
        self.click('x',"(//span[text()='新增'])[1]")
        textInput = Gtos_text(self.driver)
        textInput.click('x',"(//input[@placeholder='请选择'])[1]")
        textInput.click('x',"//span[text()='ARENS']")
        textInput.click('x',"//span[text()='保 存']")
        check.equal(self.get_text("xpath","//div[@role='alert']//h2"),"保存成功")


    def process(self,input):
        """
        流程
        """
        self.input_values()
        self.Retrieval()
        self.close_alert('未找到相关航次挂靠港数据')
        self.Add()