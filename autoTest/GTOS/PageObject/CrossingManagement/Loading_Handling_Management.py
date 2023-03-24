import time

import pytest_check as check
from Base.basepage import BasePage
from GTOS.Config import config
from GTOS.Controls.Gtos_table import Gtos_table
from GTOS.Controls.text import Gtos_text


class Loading_Management(BasePage):
    """
    直装
    """
    def loading_value(self,input):
        """
        直装内容
        """
        self.logger.info('步骤1：输入数据')
        textInput = Gtos_text(self.driver)
        textInput.select_by_label("船名航次", input["船名航次"])
        textInput.input_by_label('箱号',config.boxNumber)
        self.logger.info('步骤2：检索')
        self.click('xpath',"//span[text()='检索']")
        self.logger.info('步骤3：校验内容')
        tablecheck = Gtos_table(self.driver)
        check.equal(tablecheck.get_value('箱号'), config.boxNumber)
        check.equal(tablecheck.get_value('报道标志'),'N')
        check.equal(tablecheck.get_value('尺寸'),input['尺寸'])
        check.equal(tablecheck.get_value('箱型'),input['箱型'])
        check.equal(tablecheck.get_value('箱高'),input['箱高'])
        check.equal(tablecheck.get_value('持箱人'),input['持箱人'])
        check.equal(tablecheck.get_value('提单号'),config.boxNumber)
        check.equal(tablecheck.get_value('码头放行'),'放行')
        check.equal(tablecheck.get_value('海关放行'),'放行')
        check.equal(tablecheck.get_value('配载'),'Y')


    def loading_report(self,input):
        """
        直装报道
        """
        self.click('xpath',"(//span[contains(text(),'报道')])[1]")
        textInput = Gtos_text(self.driver)
        textInput.select_by_index('集卡编号',input['车牌'],2)
        textInput.input_by_number('集卡编号',input['集卡编号'],3)
        textInput.select_by_label('前后标志','A')
        textInput.input_by_label('联系方式','13155542223')
        textInput.select_by_label('进场道口号', 'B01')
        self.click('xpath', "(//span[contains(text(),'确认')])[6]")
        self.check_alert('报道完成')
        tablecheck = Gtos_table(self.driver)
        check.equal(tablecheck.get_value('集卡号'), input['车牌']+input['集卡编号'])
        check.equal(tablecheck.get_value('前后标志'),'后')
        check.equal(tablecheck.get_value('道口号'),'B01')
        check.equal(tablecheck.get_value('报道标志'),'Y')

