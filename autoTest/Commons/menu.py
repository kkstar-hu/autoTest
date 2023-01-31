import time

from Base.basepage import BasePage

class Menu(BasePage):
    def selectMenu(self,name):
        try:
            self.element_wait("xpath","//span[text()='"+name+"']")
            self.get_element("xpath","//span[text()='"+name+"']").click()
            time.sleep(0.3)
        except:
            raise Exception(f"未找到菜单{name}")

    def select_level_Menu(self,name):
        try:
            menuName=self.get_text("xpath","//div[@id='tags-view-container']//span[@class='tags-view-item active']").strip()
            if menuName in name:
                return
            elif "," in name:
                for x in name.split(","):
                    self.selectMenu(x)
            else: self.selectMenu(name)
            self.waitloading()
            time.sleep(1)
        except:
            try:
                self.select_level_Menu(name)
            except:
                raise Exception(f"未找到菜单{name}")