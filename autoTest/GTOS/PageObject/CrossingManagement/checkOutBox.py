import time

import pytest_check as check
from Base.basepage import BasePage
from GTOS.Config import config
from GTOS.Controls.Gtos_table import Gtos_table
from GTOS.Controls.text import Gtos_text


class CheckOutBox(BasePage):
    """
    道口管理----办理提箱手续
    """
    def select_value(self,input):
        """
        选择集卡编号、输入预约号
        """
        textInput = Gtos_text(self.driver)
        textInput.select_by_label("集卡编号", input["车牌"])
        self.get_element('xpath', "//input[@placeholder='请输入集卡号']").send_keys(input["集卡编号"])
        # self.get_element('xpath', "//input[@placeholder='请输入预约号']").send_keys(config.Number)
        textInput.search_select_by_label("箱号(前)", config.boxNumber)
        self.retrieve()

    def retrieve(self):
        """
        检索
        """
        self.click('xpath',"//span[text()='检索']")


    def input_value(self,input):
        """
        输入内容
        """
        self.logger.info('办理提箱手续：输入数据')
        textInput = Gtos_text(self.driver)
        self.click('xpath',"(//div[@class='export-cntr__buttons__right']//input)[1]")
        self.click('xpath',"//li//span[text()=\"20'普通架\"]")
        self.click('xpath', "(//div[@class='export-cntr__buttons__right']//input)[3]")
        self.click('xpath', "//li//span[text()='B01']")
        self.input_no_clear('xpath',"//input[@placeholder='请输入车架号']",'123')
        self.waitloading()
        time.sleep(1)
        textInput.select_by_label('结算人',input['结算人'])
        self.element_wait_disappear("xpath","//div[@role='alert']//p")
        self.click('xpath',"//span[text()='确认提箱']")
        self.click('xpath',"//span[contains(text(),'否')]")
        self.check_alert('清除成功')




    def process(self,input):
        """
        流程
        """
        self.select_value(input)
        self.input_value(input)
