from Base.basepage import BasePage
from Commons.Controls.table import Table
from NZYMS.config import config


class StorePlan(BasePage):

    def addStoreArea(self, input):
        self.click("xpath","//button//span[text()='检索']")
        tableleft = Table(self.driver, 2)
        tableleft.select_row("计划号", config.planNumber)
        self.click("xpath", "//div[@id='add']")
        tableRight = Table(self.driver, 3)
        tableRight.input_by_row("优先级",input["优先级"])
        tableRight.input_select_by_row("箱区",input["箱区"])
        self.click("xpath","//div[@id='save']")
        try:
            self.click("xpath","//div[@class='el-message-box__btns']/button/span[contains(text(),'确定')]")
        except:
            pass
        self.has_alert("保存成功")


