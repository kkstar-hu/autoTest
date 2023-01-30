from Base.basepage import BasePage


class Login(BasePage):

    def login(self,username,password,showName):
        if username!=None:
            self.get_elements("xpath","//input[@placeholder='Username']")[1].send_keys(username)
        if password!= None:
            self.get_elements("xpath","//input[@placeholder='Password']")[1].send_keys(password)
        self.get_elements("xpath", "//button[@class='el-button login-btn el-button--primary el-button--bg']")[1].click()
        self.waitloading()
        self.element_wait("xpath","//div[@role='alert']//p")
        self.compareValue("xpath","//div[@class='el-badge item el-dropdown-selfdefine']//span",showName)


