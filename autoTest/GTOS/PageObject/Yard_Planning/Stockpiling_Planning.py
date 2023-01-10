import time
import pytest_check as check

from selenium.webdriver import ActionChains, Keys

from Base.basepage import BasePage
from GTOS.Controls.text import Gtos_text
from GTOS.Config import config
from GTOS.Controls.Gtos_table import Gtos_table


class Stockpiling_Planning(BasePage):
    """
    堆存计划
    """
    def select_values_into(self,input):
        """
        选择计划类型，船名航次,道口进
        """
        self.logger.info('步骤1：选择计划类型，船名航次')
        textInput = Gtos_text(self.driver)
        textInput.search_select_by_label('计划类型','道口进')
        textInput.search_select_by_label('船名航次',input['堆存道口进'])

    def select_values_out(self,input):
        """
        选择计划类型，船名航次,卸船
        """
        self.logger.info('步骤1：选择计划类型，船名航次')
        textInput = Gtos_text(self.driver)
        textInput.search_select_by_label('计划类型','卸船')
        textInput.search_select_by_label('船名航次',input['堆存卸船'])

    def Retrieval(self):
        """
        检索
        """
        self.logger.info('步骤2：点击检索')
        self.click('x',"(//span[text()='检索'])[1]")


    def Add_into_plan(self):
        """
        新增堆存计划
        """
        self.logger.info('步骤3：新增堆存计划')
        self.click('x',"(//span[text()='新增'])[1]")
        tablecheck = Gtos_table(self.driver,4)
        tablecheck.tick_off_box(6)
        tablecheck.click('x',"//span[text()='生成堆存计划']")
        self.check_alert('生成堆存计划成功')

    def Add_box(self):
        """
        新增计划箱区
        """
        self.logger.info('步骤4：勾选信息，新增计划箱区')
        tablecheck = Gtos_table(self.driver,2)
        tablecheck.tick_off_box(1)
        self.click('x',"(//span[text()='新增'])[3]")
        time.sleep(1)
        self.click('x',"(//span[text()='新增'])[4]")
        time.sleep(1)
        textInput = Gtos_text(self.driver)
        textInput.input_noclear_placeholder_click('请选择','A01')
        textInput.click('x',"//span[text()='保存']")
        self.check_alert('新增成功')





    def process_into(self,input):
        """
        流程
        """
        self.select_values_into(input)
        self.Retrieval()
        self.close_alert('未找到相关堆存计划')
        self.Add_into_plan()
        self.Add_box()


    def process_out(self,input):
        self.refresh()
        self.select_values_out(input)
        self.Retrieval()
        self.close_alert('未找到相关堆存计划')
        self.Add_into_plan()
        self.Add_box()

