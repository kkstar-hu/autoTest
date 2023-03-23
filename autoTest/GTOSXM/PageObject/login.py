import time
from Base.basepage import BasePage
from GTOSXM.Controls.text import Gtos_text


class Login(BasePage):

    def login(self,username,password,showName,select=None):
        self.logger.info('步骤1输入用户名')
        if username!=None:
            self.get_elements("xpath","//input[@placeholder='Username']")[1].send_keys(username)
        self.logger.info('步骤2输入密码')
        if password!= None:
            self.get_elements("xpath","//input[@placeholder='Password']")[1].send_keys(password)
        if select!= None:
            self.get_elements("xpath","//div[@class='el-select portSelect el-select--medium']//input")[1].click()
        textInput=Gtos_text(self.driver)
        textInput.select_clickOption(select)
        self.get_elements("xpath", "//button[@class='el-button login-btn el-button--primary el-button--bg']")[1].click()
        self.waitloading()
        self.element_wait("xpath","//div[@role='alert']//p")
        self.element_wait("xpath", "(//div[@class='avatar-center avatar-center__termcd']//span)[1]")
        time.sleep(0.5)
        self.compareValue("xpath","(//div[@class='avatar-center avatar-center__termcd']//span)[1]",showName)


