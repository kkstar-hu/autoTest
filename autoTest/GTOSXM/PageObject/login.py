from Base.basepage import BasePage
from GTOSXM.Controls.text import Gtos_text


class Login(BasePage):

    def login(self, username, password, alert, select=None, showname=None):
        self.logger.info('登录：输入用户名')
        if username !=None:
            self.get_elements("xpath","//input[@placeholder='Username']")[1].send_keys(username)
        self.logger.info('登录：输入密码')
        if password != None:
            self.get_elements("xpath","//input[@placeholder='Password']")[1].send_keys(password)
        if select != None:
            self.get_elements("xpath","//div[@class='el-select portSelect el-select--medium']//input")[1].click()
            self.logger.info('登录：选择码头')
            textInput=Gtos_text(self.driver)
            textInput.select_clickOption(select)
        self.get_elements("xpath", "//button[@class='el-button login-btn el-button--primary el-button--bg']")[1].click()
        self.has_alert(alert)
        if alert == f"用户{username}登录成功":
            self.compareValue("xpath", "//div[@class='el-badge item el-dropdown-selfdefine']//span", showname)


