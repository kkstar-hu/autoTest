# -*- coding:utf-8 -*-
import time
from selenium.common import TimeoutException
from Base.basepage import BasePage

class BtosMenu(BasePage):
    def select_menu(self,name):
        try:
            self.element_wait("xpath","//span[@slot='title' and text()='"+name+"']")
        except TimeoutException as e:
            self.logger.info(f"寻找{name}菜单失败:", e)
        else:
            self.click("xpath","//span[@slot='title' and text()='"+name+"']")
            time.sleep(0.5)

    def select_level2_menu(self,name1,name2):
        try:
            self.select_menu(name1)
            self.element_wait("xpath","//span[not(@slot) and text()='"+name2+"']")
        except TimeoutException as e:
            self.logger.info(f"寻找{name2}菜单失败:", e)
        else:
            self.click("xpath","//span[not(@slot) and text()='"+name2+"']")
            time.sleep(0.5)

    def select_level3_menu(self,name1,name2,name3):
        try:
            self.select_menu(name1)
            self.select_menu(name2)
            self.element_wait("xpath","//span[not(@slot) and text()='"+name3+"']")
        except TimeoutException as e:
            self.logger.info(f"寻找{name3}菜单失败:", e)
        else:
            self.click("xpath","//span[not(@slot) and text()='"+name3+"']")
            time.sleep(0.5)