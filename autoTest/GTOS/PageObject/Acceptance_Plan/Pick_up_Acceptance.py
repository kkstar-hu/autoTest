import time

import pytest_check as check
from Base.basepage import BasePage
from GTOS.Controls.text import Gtos_text
from GTOS.Config import config
from GTOS.Controls.Gtos_table import Gtos_table


class Packing_up(BasePage):
    """
    计划受理--安排计划--提箱受理
    """
    def choice_tree(self,input):
        """
        选择计划类型
        """
        self.logger.info('步骤1：选择计划类型')
        self.click('xpath',f"//span[text()='提{input['贸易类型']}重箱计划']")

    def choice_tree_straight(self,input):
        """
        选择计划类型-直提类型
        """
        self.logger.info('步骤1：选择计划类型')
        self.click('xpath',f"//span[text()='{input['贸易类型']}箱直提计划']")

    def select_value(self,boxnumber):
        """
        选择进口船、提单号
        """
        self.logger.info('步骤2：输入航名航次')
        Gtextinput = Gtos_text(self.driver)
        Gtextinput.search_select_by_label('进口船',config.importNumber)
        Gtextinput.input_by_placeholder('提单号',boxnumber)


    def retrieve(self,input,boxnumber):
        """
        检索
        """
        self.logger.info('步骤3：检索')
        textclick = Gtos_text(self.driver)
        textclick.no_elements_click('检索')
        tablecheck = Gtos_table(self.driver,2)
        check.equal(tablecheck.get_value('箱号'),boxnumber)
        check.equal(tablecheck.get_value('海关放行'),'未放')
        check.equal(tablecheck.get_value('贸易类型'),input['贸易类型'])
        check.equal(tablecheck.get_value('尺寸'),input['尺寸'])
        check.equal(tablecheck.get_value('箱型'),input['箱型'])
        check.equal(tablecheck.get_value('箱状态'),input['箱状态'])
        check.equal(tablecheck.get_value('箱高'),input['箱高'])
        check.equal(tablecheck.get_value('持箱人'),input['持箱人'])
        check.equal(tablecheck.get_value('箱货总重'),input['箱货总重'])

    def tick_off_box(self):
        """
        勾选数据
        """
        self.logger.info('步骤4：勾选货信息数据')
        tablecheck = Gtos_table(self.driver)
        tablecheck.tick_off_box(1)

    def customs_release(self):
        """
        海关放行
        """
        self.logger.info('步骤5：海关放行')
        self.click('xpath',"//div[@class='nzctos-buttongroup']//span[text()='海关放行']")
        self.check_alert('放行成功')
        tablecheck = Gtos_table(self.driver, 2)
        check.equal(tablecheck.get_value('海关放行'), '放行')

    def generation_plan(self):
        """
        生成计划
        """
        tablecheck = Gtos_table(self.driver)
        tablecheck.tick_off_box(1)
        if self.elementExist('x',"//input[@aria-label='Press Space to toggle row selection (unchecked)']") is True:
            tablecheck.tick_off_box(1)
        self.logger.info('步骤7：生成计划')
        self.click('xpath',"//span[text()='生成计划']")
        textinput = Gtos_text(self.driver)
        textinput.select_by_label('申请人','ATL')
        textinput.select_by_label('返场类型','不返场')


    def save(self):
        """
        保存
        """
        self.logger.info('步骤8：保存计划')
        textclick = Gtos_text(self.driver)
        textclick.no_elements_click('保存')
        self.check_alert('提内贸重箱计划生成计划成功')

    def save_straight(self):
        """
        保存
        """
        self.logger.info('步骤8：保存计划')
        textclick = Gtos_text(self.driver)
        textclick.no_elements_click('保存')
        self.check_alert('内贸箱直提计划生成计划成功')


    def packing_process(self,input,boxnumber):
        """
        提箱受理流程
        """
        self.choice_tree(input)
        self.select_value(boxnumber)
        self.retrieve(input,boxnumber)
        self.tick_off_box()
        self.customs_release()
        self.generation_plan()
        self.save()

    def straight_process(self,input,boxnumber):
        """
        直提受理流程
        """
        self.choice_tree_straight(input)
        self.select_value(boxnumber)
        self.retrieve(input,boxnumber)
        self.tick_off_box()
        self.customs_release()
        self.generation_plan()
        self.save_straight()

