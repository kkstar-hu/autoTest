import pytest_check as check
from Base.basepage import BasePage
from GTOSXM.Controls.text import Gtos_text
from GTOSXM.Config import config
from GTOSXM.Controls.Gtos_table import Gtos_table


class Packing_up(BasePage):
    """
    计划受理--安排计划--提箱受理
    """
    def choice_tree(self,input):
        """
        选择计划类型
        """
        self.logger.info('计划受理-提箱受理-选择计划类型')
        self.click('xpath', f"//div[@role ='tree']//span[text() = '{input['计划类型']}']")

    def select_value(self,boxnumber):
        """
        选择进口船、提单号
        """
        self.logger.info('计划受理-提箱受理-查询')
        Gtextinput = Gtos_text(self.driver)
        Gtextinput.search_select_by_label('进口船',config.importNumber)
        Gtextinput.input_by_placeholder('提单号',boxnumber)

    def retrieve(self,input,boxnumber):
        """
        检索
        """
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
        tablecheck = Gtos_table(self.driver)
        tablecheck.tick_off_box(1)

    def customs_release(self):
        """
        海关放行
        """
        self.logger.info('计划受理-提箱受理-海关放行')
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
        self.logger.info('计划受理-提箱受理-生成计划')
        self.click('xpath',"//span[text()='生成计划']")
        textinput = Gtos_text(self.driver)
        textinput.select_by_label('申请人','ATL')
        textinput.select_by_label('返场类型','不返场')


    def save_over(self,input):
        """
        保存
        """
        self.logger.info('计划受理-提箱受理-保存计划')
        textclick = Gtos_text(self.driver)
        textclick.no_elements_click('保存')
        self.check_alert(input['alert'])


