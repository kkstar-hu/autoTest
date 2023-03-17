# -*- coding:utf-8 -*-
import time

from selenium.common.exceptions import *
from selenium.webdriver import ActionChains

from Base.basepage import BasePage

class BTOS_table(BasePage):
    def __init__(self, driver, index = 1):
        super(BTOS_table, self).__init__(driver)
        self.index = index

    # 获取行号并点击该行
    def select_row(self, header : str, value : str):
        try:
            #print(f"(//div[contains(@class, 'toscom-panel')])[{self.index}]//span[@class='vxe-cell--title' and text()='{header}']/../..")
            colid = self.get_attribute_info("xpath", f"(//div[contains(@class, 'toscom-panel')])[{self.index}]//span[@class='vxe-cell--title' and text()='{header}']/../..", "colid")
            #print(colid)
            rowid = self.get_attribute_info("xpath", f"(//div[contains(@class, 'toscom-panel')])[{self.index}]//td[@colid='{colid}']//span[contains(text(),'{value}')]/../../..","rowid")
            #print(rowid)
            e1 = self.get_elements("xpath", f"(//div[contains(@class, 'toscom-panel')])[{self.index}]//tr[@rowid='{rowid}']")[0]
        except Exception as e:
            self.logger.error("定位元素失败:", e)
        else:
            # print(f"(//div[contains(@class, 'toscom-panel')])[{self.index}]//tr[@rowid='{rowid}']")
            ActionChains(self.driver).click(e1).perform()
            return rowid

    def get_value_by_rowid(self, rowid : str, header : str):
        try:
            colid = self.get_attribute_info("xpath", f"(//div[contains(@class, 'toscom-panel')])[{self.index}]//span[@class='vxe-cell--title' and text()='{header}']/../..", "colid")
        except Exception as e:
            self.logger.error("定位元素失败:", e)
        else:
            return self.get_attribute_info("xpath", f"(//div[contains(@class, 'toscom-panel')])[{self.index}]//tr[@rowid='{rowid}']/td[@colid='{colid}']//span", 'textContent')

    def click_header_button(self, name : str):
        try:
            e1 = self.get_element_wait("xpath", f"(//div[contains(@class, 'toscom-panel')])[{self.index}]//div[@class='toscom-buttongroup']//span[text()='{name}']/..")
        except Exception as e:
            self.logger.error("定位元素失败:", e)
        else:
            e1.click()

    def click_inner_button(self, rowid : str, name : str):
        try:
            e1 = self.get_element_wait("xpath", f"(//div[contains(@class, 'toscom-panel')])[{self.index}]//tr[@rowid='{rowid}']//span[text()='{name}']/..")
        except Exception as e:
            self.logger.error("定位元素失败:", e)
        else:
            e1.click()
