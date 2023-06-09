import pytest_check as check
from Base.basepage import BasePage
from GTOSXM.Config import config
from GTOSXM.Controls.Gtos_table import Gtos_table
from GTOSXM.Controls.text import Gtos_text


class StraightLoad_StraightLift_Management(BasePage):
    """
    直装/直提
    """

    def loading_value(self, input, boxnumber):
        """
        直装内容
        """
        self.logger.info('直装直提管理-查询')
        textInput = Gtos_text(self.driver)
        textInput.search_select_by_label("船名航次", config.outportNumber)
        textInput.input_by_label('箱号', boxnumber)
        self.click('xpath', "//span[text()='检索']")
        tablecheck = Gtos_table(self.driver)
        check.equal(tablecheck.get_value('箱号'), boxnumber)
        check.equal(tablecheck.get_value('报道标志'), 'N')
        check.equal(tablecheck.get_value('尺寸'), input['尺寸'])
        check.equal(tablecheck.get_value('箱型'), 'GP')
        check.equal(tablecheck.get_value('箱高'), input['箱高'])
        check.equal(tablecheck.get_value('持箱人'), input['持箱人'])
        check.equal(tablecheck.get_value('提单号'), boxnumber)
        check.equal(tablecheck.get_value('码头放行'), '放行')
        check.equal(tablecheck.get_value('海关放行'), '放行')

    def lifting_value(self, input, boxnumber):
        """
        直提内容
        """
        self.logger.info('直装直提管理-查询')
        textInput = Gtos_text(self.driver)
        textInput.search_select_by_label("船名航次", config.importNumber)
        textInput.input_by_label('箱号', boxnumber)
        self.logger.info('直装直提管理：检索')
        self.click('xpath', "//span[text()='检索']")
        tablecheck = Gtos_table(self.driver, 2)
        check.equal(tablecheck.get_value('箱号'), boxnumber)
        check.equal(tablecheck.get_value('报道标志'), 'N')
        check.equal(tablecheck.get_value('尺寸'), input['尺寸'])
        check.equal(tablecheck.get_value('箱型'), input['箱型'])
        check.equal(tablecheck.get_value('箱高'), input['箱高'])
        check.equal(tablecheck.get_value('持箱人'), input['持箱人'])

    def loading_report(self, input):
        """
        直装报道
        """
        self.logger.info('直装直提管理-直装报到')
        self.click('xpath', "(//span[contains(text(),'报道')])[1]")
        textInput = Gtos_text(self.driver)
        textInput.select_by_index('集卡编号', input['车牌'], 2)
        textInput.input_by_number('集卡编号', input['集卡编号'], 3)
        textInput.select_by_label('前后标志', 'A')
        textInput.input_by_label('联系方式', '13155542223')
        textInput.select_by_label('进场道口号', 'G12')
        self.click('xpath', "//button[@class='el-button el-button--primary el-button--small']")
        self.check_alert('报道完成')
        tablecheck = Gtos_table(self.driver)
        check.equal(tablecheck.get_value('集卡号'), input['车牌'] + input['集卡编号'])
        check.equal(tablecheck.get_value('前后标志'), '后')
        check.equal(tablecheck.get_value('道口号'), 'G12')
        check.equal(tablecheck.get_value('报道标志'), 'Y')
        check.equal(tablecheck.get_value('联系方式'), '13155542223')

    def lifting_report(self, input):
        """
        直提报道
        """
        self.logger.info('直装直提管理-直提报到')
        self.click('xpath', "(//span[contains(text(),'报道')])[3]")
        textInput = Gtos_text(self.driver)
        textInput.select_by_index('集卡编号', input['车牌'], 2)
        textInput.input_by_number('集卡编号', input['集卡编号'], 3)
        textInput.select_by_label('前后标志', 'A')
        textInput.input_by_label('联系方式', '13155542223')
        textInput.select_by_label('进场道口号', 'G12')
        self.click('xpath', "//button[@class='el-button el-button--primary el-button--small']")
        self.check_alert('报道完成')
        tablecheck = Gtos_table(self.driver, 2)
        check.equal(tablecheck.get_value('集卡号'), input['车牌'] + input['集卡编号'])
        check.equal(tablecheck.get_value('前后标志'), '后')
        check.equal(tablecheck.get_value('道口号'), 'G12')
        check.equal(tablecheck.get_value('报道标志'), 'Y')
        check.equal(tablecheck.get_value('联系方式'), '13155542223')

    def switch_lift(self):
        """
        切换直提
        """
        self.click('xpath', "//div[contains(text(),'直提列表')]")
