import json
import time
import pytest_check as check
from selenium.webdriver import ActionChains

from Base.basepage import BasePage
from GTOSXM.Config.config import takeNumber
from GTOSXM.Controls.text import Gtos_text
from GTOSXM.Config import config
from GTOSXM.Controls.Gtos_table import Gtos_table

class Structure_Stowage(BasePage):
    """
    有结构船舶配载
    """
    def Retrieve(self,input):
        """
        输入内容，检索
        """
        self.logger.info('有结构船舶配载-查询：'+ input["船舶代码"])
        textinput = Gtos_text(self.driver)
        textinput.search_select_by_label('船舶查询',input["船舶中文名称"])
        self.click('xpath',"//button//span[text()='检索']")
        textinput.left_click('x',f"//div[text()='{config.importNumber}']")
        self.click('xpath',"//span[text()='确 认']")
        self.click('x',"//div[text()=' 箱列表 ']")


    def mouse_job(self):
        """
        框选操作
        """
        self.logger.info('有结构船舶配载-框选')
        self.clickandhold("x","//div[@data-hno='01']")
        self.move_mouse_to_element("x","//div[@data-hno='05']")
        self.move_release()
        time.sleep(3)

    def mouse_job_once(self):
        """
        框选操作
        """
        self.logger.info('有结构船舶配载-查看接口配载情况')
        self.clickandhold("x","//div[@data-hno='01']")
        self.move_mouse_to_element("x","//div[@data-hno='05']")
        self.move_release()
        time.sleep(1)

    def send_box(self):
        """
        配载发送
        """
        self.click('x',"//span[text()='发送']")
        time.sleep(1)
        self.click('x', "//span[text()='整船发送']")
        self.check_alert('发送成功')
        self.close_alert('发送成功')

    def choice_table(self):
        """
        选择箱位置
        """
        self.click('x',"//div[contains(text(),'箱列表')]")
        self.click('x',"//div[contains(text(),'场外箱')]")

