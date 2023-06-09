from Base.basepage import BasePage
from GTOS.Controls.text import Gtos_text


class Login(BasePage):

    def login(self,username,password,showName,select=None):
        if username!=None:
            self.get_elements("xpath","//input[@placeholder='Username']")[1].send_keys(username)
        if password!= None:
            self.get_elements("xpath","//input[@placeholder='Password']")[1].send_keys(password)
        if select!= None:
            self.get_elements("xpath","//div[@class='el-select portSelect el-select--medium']//input")[1].click()
        textInput = Gtos_text(self.driver)
        textInput.select_clickOption(select)
        self.get_elements("xpath", "//button[@class='el-button login-btn el-button--primary el-button--bg']")[1].click()
        self.waitloading()
        self.element_wait("xpath","//div[@role='alert']//p")
        self.compareValue("xpath","//div[@class='el-badge item el-dropdown-selfdefine']//span",showName)


