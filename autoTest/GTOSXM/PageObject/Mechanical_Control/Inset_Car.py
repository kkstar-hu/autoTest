
import time

import pytest_check as check
from selenium.webdriver import ActionChains

from Base.basepage import BasePage
from GTOSXM.Controls.text import Gtos_text
from GTOSXM.Config import config
from GTOSXM.Controls.Gtos_table import Gtos_table

class Inset_Car(BasePage):
    """
    查看可用集卡
    """
    def choice_job(self,name):
        '''
        选择作业路
        '''
        self.logger.info('内集卡控制-查看可用内集卡号')
        em = self.get_element('x',f"//div[text()='{name}']")
        ActionChains(self.driver).move_to_element(em).click().perform()

    def choice_car(self):
        '''
        选择可用集卡号
        '''
        list1 = []
        row = []
        value = self.get_element('x',"(//div[@class='ag-center-cols-container'])[2]")
        value_text = list(value.get_attribute('textContent').split('Q002'))
        del value_text[0]
        # print(value_text)
        for i in value_text:
            if '等待装车' in i:
                row.append(value_text.index(i))
        # print(row)
        car_value = self.get_element('x',"(//div[@class='ag-pinned-left-cols-container'])[2]")
        car_text = car_value.get_attribute('textContent').replace(' ','').split('\n')
        for i in car_text:
            if len(i) >= 2:
                list1.append(i[0:4])
        # print(list1)
        # print(list1[row[0]])
        config.carnumber = list1[row[1]]



