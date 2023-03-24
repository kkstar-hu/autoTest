import pytest_check as check
from Base.basepage import BasePage
from selenium.webdriver.common.keys import Keys
from Commons.Controls.table import Table
from Commons.Controls.text import text
from NZYMS.config import config

class Mention_Box_registration(BasePage):
    """道口管理-----提箱进场登记"""

    def mention_box_plan(self,input):
        """
        有计划提箱进场登记
        """
        self.logger.info('提箱计划:输入已有计划的箱号')
        textInput = text(self.driver)
        textInput.input_by_number("箱号", config.boxNumber)
        self.get_element('xpath', '//input[@placeholder="请输入箱号"]').send_keys(Keys.ENTER)
        if input['车牌'] is not None:
            textInput.select_by_label("车牌", input['车牌'])
        if input['车号'] is not None:
            self.get_element('xpath', "//input[@placeholder='请输入车号']").send_keys(input['车号'])
        if input['手机号'] is not None:
            self.get_element('xpath', '//input[@placeholder="请输入手机号"]').send_keys(input['手机号'])
        self.waitloading()
        tableCheck=Table(self.driver,3)
        self.logger.info('check2：验证添加后列表的值正确')
        check.is_in(tableCheck.get_value('计划号',),config.outplanNumber)
        check.equal(tableCheck.get_value("箱号"), config.boxNumber)
        tableCheck1 = Table(self.driver,2)
        check.is_in(tableCheck1.get_value("尺寸"), input['尺寸'])
        check.is_in(tableCheck1.get_value("箱型"), input['箱型'])
        check.is_in(tableCheck1.get_value("持箱人"), input['持箱人'])
        check.equal(tableCheck1.get_value("空重"), input['空重'])

    def select_values(self, input):
        """
        道口选择功能,手机输入，车辆选择（写死了）
        """
        self.logger.info('道口选择：选择道口（进场专用/01）,车牌，手机号')
        textInput = text(self.driver)
        if input['堆场'] is not None:
            textInput.select_by_label("堆场", input["堆场"])
        if input['道口'] is not None:
            textInput.select_by_label("道口", input['道口'])

    def  confirm_button(self,input):
        """
        提箱确认按钮
        """
        self.logger.info('提箱计划：提箱确认')
        self.get_element('xpath', "//span[text()='提箱确认']").click()
        self.check_alert(input["outboxalert"])

