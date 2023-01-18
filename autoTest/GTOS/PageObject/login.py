from Base.basepage import BasePage


class Login(BasePage):

    def login(self,username,password,showName):
        self.logger.info('步骤1输入用户名')
        if username!=None:
            self.get_elements("xpath","//input[@placeholder='Username']")[1].send_keys(username)
        self.logger.info('步骤2输入密码')
        if password!= None:
            self.get_elements("xpath","//input[@placeholder='Password']")[1].send_keys(password)
        self.get_elements("xpath", "//button[@class='el-button login-btn el-button--primary el-button--bg']")[1].click()
        self.waitloading()
        self.element_wait("xpath","//div[@role='alert']//p")
        self.compareValue("xpath","//div[@class='el-badge item el-dropdown-selfdefine']//span",showName)


