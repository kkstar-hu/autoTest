from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from Base.basepage import BasePage
from Commons.utils import get_distance
import base64
import time

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


