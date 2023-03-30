# -*- coding:utf-8 -*-
import time
from selenium.common import TimeoutException
from Base.basepage import BasePage

class BtosMenu(BasePage):
    def select_menu(self,name):
        try:
            self.element_wait("xpath","//span[@slot='title' and text()='"+name+"']")
        except Exception:
            self.logger.error(f"寻找菜单{name}失败:", exc_info=True)
        else:
            self.click("xpath","//span[@slot='title' and text()='"+name+"']")
            time.sleep(0.5)

    def select_level2_menu(self,name1,name2):
        try:
            self.select_menu(name1)
            self.element_wait("xpath","//span[not(@slot) and text()='"+name2+"']")
        except Exception:
            self.logger.info(f"寻找菜单{name2}失败:", exc_info=True)
        else:
            self.click("xpath","//span[not(@slot) and text()='"+name2+"']")
            time.sleep(0.5)

    def select_level3_menu(self,name1,name2,name3):
        try:
            self.select_menu(name1)
            self.select_menu(name2)
            self.element_wait("xpath","//span[not(@slot) and text()='"+name3+"']")
        except Exception:
            self.logger.info(f"寻找菜单{name3}失败:", exc_info=True)
        else:
            self.click("xpath","//span[not(@slot) and text()='"+name3+"']")
            time.sleep(0.5)

