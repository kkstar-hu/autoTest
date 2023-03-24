from Base.basepage import BasePage
from Commons.Controls.text import text


class Cars_Registration(BasePage):  #车辆进场登记

    def select_values(self,input):
        """
        道口选择功能,手机输入，车辆选择
        """
        self.logger.info('车辆道口：选择道口（进场专用/01）,车牌，手机号')
        textInput = text(self.driver)
        if input['堆场'] is not None:
            textInput.select_by_label("堆场", input["堆场"])
        if input['道口'] is not None:
            textInput.select_by_label("道口", input['道口'])
        if input['车牌'] is not None:
            textInput.select_by_label("车牌号", input['车牌'])
        if input['车号'] is not None:
            self.get_element('xpath', "//input[@placeholder='请输入车号']").send_keys(input['车号'])
        if input['手机号'] is not None:
            self.get_element('xpath', '//input[@placeholder="请输入手机号"]').send_keys(input['手机号'])

    def goin_noplan(self):
        """无任务进场"""
        self.click('xpath',"//span[text()='无任务进场']")

    def goin_mentionplan(self):
        """提货进场"""
        self.click('xpath', "//span[text()='提货进场']")

    def goin_sendplan(self):
        """送货进场"""
        self.click('xpath', "//span[text()='送货进场']")

    def into_process(self,input):
        """送货进场"""
        self.select_values(input)
        self.goin_sendplan()

    def out_process(self,input):
        """提货进场"""
        self.select_values(input)
        self.goin_mentionplan()