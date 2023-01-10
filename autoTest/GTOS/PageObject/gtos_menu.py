import time

from Base.basepage import BasePage
from Commons.menu import Menu


class GtosMenu(Menu):

    def selectMenu(self, name):
        if self.elementExist("xpath", "//li[@role='menuitem']//span[text()='" + name + "']"):
            self.get_element("xpath", "//li[@role='menuitem']//span[text()='" + name + "']").click()
            self.waitloading()
            time.sleep(0.3)
            return
        elif self.elementExist("xpath", "//div[@class='left-menu']//button[@style='display: none;']"):
            for i in range(1, 13):
                self.click("xpath", "//i[@classs='el-icon el-icon-d-arrow-right']")
        elif self.elementExist("xpath", "//div[@class='right-menu']//button[@style='display: none;']"):
            for i in range(1, 13):
                self.click("xpath", "//i[@classs='el-icon el-icon-d-arrow-left']")
        else:
            raise Exception(f"未找到菜单{name}")

    def select_level_Menu(self,name):
        try:
            menuName=self.get_text("xpath","//div[@id='tags-view-container']//span[starts-with(@class,'tags-view-item active')]").strip()
            if menuName in name:
                return
            elif "," in name:
                for x in name.split(","):
                    self.selectMenu(x)
            else: self.selectMenu(name)
            self.waitloading()
            time.sleep(1)
        except:
            raise Exception(f"未找到菜单{name}")