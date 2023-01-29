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

    def search(self,type,number):
        """
        选择计划类型，船名航次,道口进
        """
        self.logger.info('步骤1：选择计划类型，船名航次')
        textInput = Gtos_text(self.driver)
        textInput.select_by_label('计划类型', type)
        textInput.search_select_by_label('船名航次', number)
        self.click('x', "(//span[text()='检索'])[1]")

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
        self.close_alert('生成堆存计划成功')

    def Add_box_INTO(self):
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
        self.refresh()
        self.search("道口进",config.outportNumber)
        tablecheck.tick_off_box(1)
        self.click('x',"(//span[text()='新增'])[3]")
        time.sleep(1)
        self.click('x',"(//span[text()='新增'])[4]")
        time.sleep(1)
        textInput = Gtos_text(self.driver)
        textInput.input_noclear_placeholder_click('请选择','A01')
        textInput.click('x',"//span[text()='保存']")
        self.check_alert('新增成功')
        self.close_alert('新增成功')


    def Add_box_OUT(self):
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
        self.close_alert('新增成功')


    def process_into(self):
        """
        流程
        """
        self.search("道口进",config.outportNumber)
        self.close_alert('未找到相关堆存计划')
        self.Add_into_plan()
        self.Add_box_INTO()


    def process_out(self):
        self.search("卸船",config.importNumber)
        # self.close_alert('未找到相关堆存计划')
        self.Add_into_plan()
        self.Add_box_OUT()

