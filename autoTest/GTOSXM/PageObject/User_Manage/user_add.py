import pytest_check as check

from Base.basepage import BasePage
from GTOSXM.Controls.Gtos_table import Gtos_table
from GTOSXM.Controls.text import Gtos_text


class User_Manage(BasePage):
    def Add_User(self, input):
        self.click('xpath',"//span[contains(text(),'新增用户')]")  #点击新增
        textInput = Gtos_text(self.driver)  #输入新增用户信息
        textInput.input_by_label("用户账号", input["用户账号"])  #输入框
        textInput.input_by_label("用户名称", input["用户名称"])
        textInput.input_by_label("用户密码", input["用户密码"])
        textInput.select_by_label("用户状态", input["用户状态"])  #单选框
        textInput.select_by_label("归属码头", input["归属码头"])
        textInput.select_by_label("操作码头", input["操作码头"])
        self.click('x', "//span[@class='el-checkbox__label' and text()='测试']")  #多选框
        self.save()  #点击保存
        # self.check_alert("添加成功")  #校验是否添加成功
        self.logger.info('校验新用户信息')
        tablecheck = Gtos_table(self.driver, 1)  # 校验信息是否正确
        rowId = tablecheck.select_row('用户账号',input['用户账号'])
        check.equal(tablecheck.get_value_by_rowid(rowId,'用户账号'), input['用户账号'])
        check.equal(tablecheck.get_value('名称'), input['名称'])
        check.equal(tablecheck.get_value('用户状态'), input['用户状态'])
        check.equal(tablecheck.get_value('归属码头'), input['归属码头'])
        check.equal(tablecheck.get_value('操作码头'), input['操作码头'])

    def New_User_Select(self, input):
        tablecheck = Gtos_table(self.driver, 1)  # 校验信息是否正确
        usercoun = input['用户账号']
        self.scroll_to_view("//div[@class='ag-center-cols-container'][1]//div[@col-id='sur_useraccount' and text()='testAddUser8']")
        # self.scroll_to_view(f"//div[@class='ag-center-cols-container'][1]//div[@col-id='sur_useraccount' and text()='{usercoun}']")
        rowId = tablecheck.select_row('用户账号', input['用户账号'])
        check.equal(tablecheck.get_value_by_rowid(rowId, '用户账号'), input['用户账号'])
        #
        # check.equal(tablecheck.get_value('用户账号'), input['用户账号'])
        # check.equal(tablecheck.get_value('名称'), input['名称'])
        # check.equal(tablecheck.get_value('用户状态'), input['用户状态'])
        # check.equal(tablecheck.get_value('归属码头'), 'XRCT')
        # check.equal(tablecheck.get_value('操作码头'), 'XRCT')




