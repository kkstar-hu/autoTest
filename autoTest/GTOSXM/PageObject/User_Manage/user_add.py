import pytest_check as check

from Base.basepage import BasePage
from GTOSXM.Controls.text import Gtos_text


class User_Manage(BasePage):
    def Add_User(self, input):
        #点击新增
        self.click('xpath',"//span[contains(text(),'新增用户')]")
        #输入新增用户信息
        textInput = Gtos_text(self.driver)
        textInput.select_by_label("用户账号", input["用户账号"])
        textInput.select_by_label("用户名称", input["用户名称"])
        textInput.select_by_label("用户密码", input["用户密码"])
        textInput.select_clickOption("正常")
        textInput.select_clickOption("海润")
        textInput.select_clickOption("海润")
        textInput.select_clickOption("测试")
        #点击保存
        textInput.click('x', "//span[contains(text(),'保 存')]")
        #校验是否添加成功
        check.equal(self.get_text("xpath", "//div[@role='alert']//h2"), "添加成功")

