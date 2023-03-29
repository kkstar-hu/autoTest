import time

import pytest_check as check
from selenium.webdriver import ActionChains

from Base.basepage import BasePage
from GTOSXM.Controls.Gtos_table import Gtos_table
from GTOSXM.Controls.text import Gtos_text


class User_Manage(BasePage):
    def Add_User(self, input):
        self.click('xpath', "//span[contains(text(),'新增用户')]")  #点击新增
        textInput = Gtos_text(self.driver)  #输入新增用户信息
        textInput.input_by_label("用户账号", input["用户账号"])  #输入框
        textInput.input_by_label("用户名称", input["用户名称"])
        textInput.input_by_label("用户密码", input["用户密码"])
        textInput.select_by_label("用户状态", input["用户状态"])  #单选框
        textInput.select_by_label("归属码头", input["归属码头"])
        textInput.select_by_label("操作码头", input["操作码头"])
        self.click('x', "//span[@class='el-checkbox__label' and text()='测试']")  #多选框
        self.save()  #点击保存
        self.check_alert("添加成功")  #校验是否添加成功
        self.logger.info('校验新用户信息')


    def New_User_Select(self, input):
        value = input['用户账号']
        e1 = self.get_element('xpath',"//input[@aria-label='用户账号 Filter Input']")
        ActionChains(self.driver).click(e1).send_keys(value).perform()
        self.element_wait('xpath',f"//div[text()='{value}']")
        tablecheck = Gtos_table(self.driver, 1)
        check.equal(tablecheck.get_value('用户账号'), input['用户账号'])
        # check.equal(tablecheck.get_value('名称'), input['名称'])
        # check.equal(tablecheck.get_value('用户状态'), input['用户状态'])
        # check.equal(tablecheck.get_value('归属码头'), input['归属码头'])
        # check.equal(tablecheck.get_value('操作码头'), input['操作码头'])
        web_role = self.get_elements('x', "//span[@class='el-tree-node__label']")
        print(web_role)
        role = input['绑定角色']
        role.sort()
        i = 0
        while i < len(web_role):
            if web_role[i] is role[i]:
                print("web_role"+web_role[i]+"与"+role[i]+"相符")
            else:
                print("web_role"+web_role[i]+"与"+role[i]+"不相符")

        # i = 0
        # while i < len(role):
        #     self.elementExist('x', f"//span[text()='{role[i]}' and @class='el-tree-node__label']")
        #     i += 1

    def Update_User(self, input):
        self.click('xpath', "//span[text()='修改']") #点击修改
        textInput = Gtos_text(self.driver)  # 输入更新的用户信息
        textInput.input_by_label("显示名称", input["显示名称"])  # 输入框
        textInput.input_by_label("归属码头", input["更新的归属码头"])
        self.click('x', "//span[@class='el-checkbox__label' and text()='开发员']")  # 多选框
        self.click('x', "//span[@class='el-checkbox__label' and text()='系统管理员']")
        self.save()  # 点击保存
        self.check_alert("修改成功")  # 校验是否修改成功
        value = input['用户账号']
        e1 = self.get_element('xpath', "//input[@aria-label='用户账号 Filter Input']")
        ActionChains(self.driver).click(e1).send_keys(value).perform()
        self.element_wait('xpath', f"//div[text()='{value}']")
        tablecheck = Gtos_table(self.driver, 1)
        check.equal(tablecheck.get_value('用户账号'), input['用户账号'])
        check.equal(tablecheck.get_value('名称'), input['显示名称'])
        check.equal(tablecheck.get_value('用户状态'), input['用户状态'])
        check.equal(tablecheck.get_value('归属码头'), input['更新的归属码头'])
        check.equal(tablecheck.get_value('操作码头'), input['操作码头'])

        role = input['绑定角色']
        i = 0
        while i < len(role):
            self.elementExist('x', f"//span[text()='{role[i]}' and @class='el-tree-node__label']")
            i += 1









