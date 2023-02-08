import time

import pytest_check as check
from selenium.webdriver.common.by import By

from Base.basepage import BasePage
from GTOS.Controls.text import Gtos_text
from GTOS.Config import config
from GTOS.Controls.Gtos_table import Gtos_table


class Direct_loading_mention_Management(BasePage):
    """
    直装/直提管理
    """
    def Direct_loading(self,input):
        """
        直装内容
        """
        self.logger.info('直装/直提管理-输入航名航次查询')
        textinput = Gtos_text(self.driver)
        # textinput.input_noclear_placeholder_click('请选择',input['直装直提船名航次'])
        # textinput.input_by_label('箱号', config.boxNumber)
        # a = self.get_element('xpath',"//input[@placeholder='请输入箱号']")
        self.driver.find_element(By.XPATH, "//input[@placeholder='请输入箱号']")


