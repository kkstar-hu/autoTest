
import pytest_check as check
from Base.basepage import BasePage
from GTOS.Controls.text import Gtos_text



class CloseFlight(BasePage):

    def search(self,number):
        """
        输入内容，检索
        """
        self.logger.info('关闭航次：输入航名航次')
        textinput = Gtos_text(self.driver)
        textinput.search_select_by_label('船名航次',number)
        self.logger.info('关闭航次：检索')
        self.click('xpath', "//span[text()='检索']")


    def closeFlight(self):
        self.click('xpath', "//span[text()='航次关闭']")
        self.check_alert("航次关闭结果：共计2个箱，关闭成功！资料箱归档0个, 溢箱0个, 缺箱0个。")
