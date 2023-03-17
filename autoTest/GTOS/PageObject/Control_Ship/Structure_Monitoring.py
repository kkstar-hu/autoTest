import time
import pytest_check as check
from selenium.webdriver import ActionChains
from Base.basepage import BasePage
from Commons.DateTime import DataTime
from GTOS.Controls.text import Gtos_text
from GTOS.Config import config
from GTOS.Controls.Gtos_table import Gtos_table

class Structure_Monitoring(BasePage):
    """
    有结构船舶监控
    """
    def Retrieve(self,input):
        """
        输入内容，检索
        """
        self.logger.info('有结构船舶监控-查询：'+ input["船舶代码"])
        textinput = Gtos_text(self.driver)
        textinput.search_select_by_label('船舶查询',input["船舶代码"])
        self.click('xpath',"//span[text()='检索']")
        textinput.left_click('x',f"//div[text()='{config.importNumber}']")
        self.click('xpath',"//span[text()='确 认']")
        self.check_alert('检查通过')
        self.close_alert('检查通过')


    def Send_Box(self,input,boxnumber):
        """
        发箱
        """
        self.logger.info('无结构船舶监控-卸船发箱'+boxnumber)
        table = Gtos_table(self.driver, 3)
        table.check2("箱号", boxnumber)
        self.click('id',"shipmentconfirm")
        self.check_alert('发箱成功')
        rowid = table.select_row2("箱号", boxnumber)
        check.equal(table.get_value_by_rowid(rowid,'作业状态'), '等待作业')

    def LadeShip_Send_Box(self,boxnumber):
        """
        发箱
        """
        self.logger.info('有结构船舶监控-装船发箱'+boxnumber)
        table = Gtos_table(self.driver)
        table.left_click('x',"//span[text()='发箱']")
        time.sleep(1)
        table.left_click('id',"send-hatch")
        time.sleep(1)
        text = Gtos_text(self.driver)
        text.select_by_label('舱号','01')
        text.select_by_label('CWP','A101')
        self.click('x',"//span[text()='查找']")
        table.check('箱号',boxnumber)
        tablecheck = Gtos_table(self.driver)
        if  boxnumber == config.boxNumber:
            check.equal(tablecheck.get_value_by_rowid(config.boxNumber, '作业状态'), '可作业')
            self.click('x',"//button//span[text()='发箱']")
            self.check_alert('发箱成功')
            self.close_alert('发箱成功')
            check.equal(tablecheck.get_value_by_rowid(config.boxNumber, '作业状态'), '发箱')
        if  boxnumber == config.outBoxNumber:
            check.equal(tablecheck.get_value_by_rowid(config.outBoxNumber, '作业状态'), '提交中控')
            self.click('x',"//button//span[text()='发箱']")
            self.check_alert('发箱成功')
            self.close_alert('发箱成功')
            check.equal(tablecheck.get_value_by_rowid(config.outBoxNumber, '作业状态'), '发箱')


