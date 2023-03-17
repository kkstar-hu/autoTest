import time
import pytest_check as check
from selenium.webdriver import ActionChains

from Base.basepage import BasePage
from GTOS.Config.config import takeNumber
from GTOS.Controls.text import Gtos_text
from GTOS.Config import config
from GTOS.Controls.Gtos_table import Gtos_table

class Structure_Stowage(BasePage):
    """
    有结构船舶配载
    """
    def Retrieve(self,input):
        """
        输入内容，检索
        """
        self.logger.info('有结构船舶监控-查询：'+ input["船舶代码"])
        textinput = Gtos_text(self.driver)
        textinput.search_select_by_label('船舶查询',input["船舶代码"])
        self.click('xpath',"//button//span[text()='检索']")
        textinput.left_click('x',f"//div[text()='{config.importNumber}']")
        self.click('xpath',"//span[text()='确 认']")
        self.click('x',"//div[text()=' 箱列表 ']")


    def refresh_peizai(self):
        """
        接口配载，刷新查看结果
        """
        self.click('id',"refreshConList")
        time.sleep(0.5)
        self.click('x',"//span[text()='发送']")
        time.sleep(0.5)
        self.click('x',"//span[text()='整船发送']")
        self.check_alert('发送成功')
        self.close_alert('发送成功')




