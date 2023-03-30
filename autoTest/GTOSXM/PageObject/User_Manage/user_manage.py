import time

import pytest_check as check
from Base.basepage import BasePage
from GTOSXM.Controls.Gtos_table import Gtos_table
from GTOSXM.Controls.text import Gtos_text
from GTOSXM.PageObject.login import Login
from GTOSXM.TestCase.conftest import driver


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

    def User_Search(self, input):
        self.left_clickandsend('xpath', "//input[@aria-label='用户账号 Filter Input']", input['用户账号'])
        self.element_wait('xpath', f"//div[text()='{input['用户账号']}']")

    def User_Check(self, input):
        tablecheck = Gtos_table(self.driver, 1)
        check.equal(tablecheck.get_value('用户账号'), input['用户账号'])
        check.equal(tablecheck.get_value('名称'), input['名称'])
        check.equal(tablecheck.get_value('用户状态'), input['用户状态'])
        check.equal(tablecheck.get_value('归属码头'), input['归属码头'])
        check.equal(tablecheck.get_value('操作码头'), input['期望操作码头'])

    def Check_Role(self, input):
        """取出界面上用户所拥有的全部角色元素"""
        web_role = self.get_elements('x', "//div[@class='el-tree-node__children']//span[@class='el-tree-node__label']")
        print(web_role)
        role_list = list()
        i = 0
        while i < len(web_role):
            print(web_role[i].text)
            str_role = web_role[i].text  # 取出角色元素的文本即界面上的角色名
            role_list.append(str_role)  # 将角色名放进role_list里
            i += 1

        role_list.sort()  # 对role_list进行一个排序
        print(role_list)
        role = input['期望绑定角色']  # 取出data里的角色
        role = role.split(",")  # 将data里的角色转换成list
        role.sort()  # 排序
        print(role)

        """将界面的角色与data里的角色进行比对"""
        i = 0
        while i < len(role_list):
            if role_list[i] == role[i]:
                print("role_list：" + role_list[i] + "与" + role[i] + "相符")
                i += 1
            else:
                print("role_list：" + role_list[i] + "与" + role[i] + "不相符")
                break


    def Update_User(self, input):
        self.left_clickandsend('xpath', "//input[@aria-label='用户账号 Filter Input']", input['用户账号'])
        self.element_wait('xpath', f"//div[text()='{input['用户账号']}']")
        self.left_click('xpath', "//span[text()='修改']")
        textInput = Gtos_text(self.driver)  # 输入更新的用户信息
        textInput.input_by_label("显示名称", input["用户名称"])  # 输入框
        textInput.select_by_label("归属码头", input["归属码头"])
        textInput.select_by_label_time("操作码头", input["操作码头"])
        role = input["绑定角色"]
        self.click('x', f"//span[@class='el-checkbox__label' and text()='{role}']")  # 多选框
        self.save()  # 点击保存
        self.check_alert("修改成功")  # 校验是否修改成功

    def Forbidden_User(self, input):
        self.left_click('x', "//span[text()='禁用']")
        message_element = self.get_element('x', "//div[@class='el-message-box__message']")
        message = message_element.text
        print(message)
        data_message = "此操作将禁用用户："+input["用户名称"]+"，是否继续?"
        print(data_message)
        if message == data_message:
            self.left_click('x', "//span[text()=' 确定 ']")
        else:
            print("禁用用户与弹窗信息不匹配！")
        self.elementExist("x","//div[@class='nzctos-grid__operation__column-container']//div[@class='buttongroup__item'][3]")  #判断界面元素存在”恢复“

    def Logout_User(self):
        self.click('x', "//i[@class='el-icon-user user-avatar']")  #点击用户头像
        self.click('x', "//span[text()='退出登录']")  #点击退出登录
        self.click('x', "//button[@type='button']//span[text()=' 退出 ']")

    def Login_As_Forbidden_User(self, input):
        forbidden_driver = Login(driver)
        forbidden_driver.login(input["用户账号"], input["密码"], input["归属码头"], input["码头中文名称"])
        self.wait_element_appear('x', "//div[@role='alert']")
        self.check_alert("账户已被禁用。账户:"+input["用户账号"])


