import time
import pytest_check as check
from Base.basepage import BasePage
from Commons.Controls.tag import Tag
from GTOS.Controls.text import Gtos_text
from GTOS.Config import config
from GTOS.Controls.Gtos_table import Gtos_table


class Manifest(BasePage):
    """
    出口资料-装船箱放行
    """

    def input_values(self, input, boxnumber):
        """
        输入出口船名航次、箱号
        """
        self.logger.info('装船箱放行：查询航次')
        Gtextinput = Gtos_text(self.driver)
        Gtextinput.search_select_by_label('出口船名航次', config.outportNumber)
        Gtextinput.input_by_label('箱号', boxnumber)
        self.click('xpath', "//span[text()='检索']")
        tablecheck = Gtos_table(self.driver)
        tablecheck.tick_off_box(1)
        check.equal(tablecheck.get_value('提单号'), boxnumber)
        check.equal(tablecheck.get_value('预配数'), '0')
        check.equal(tablecheck.get_value('放行'), '未放')
        check.equal(tablecheck.get_value('卸货港'), input['卸货港'])
        tablecheck1 = Gtos_table(self.driver, 2)
        check.equal(tablecheck1.get_value('箱号'), boxnumber)
        check.equal(tablecheck1.get_value('放行'), '未放')
        check.equal(tablecheck1.get_value('卸货港'), input['卸货港'])
        check.equal(tablecheck1.get_value('贸易类型'), input['贸易类型'][3:5])
        check.equal(tablecheck1.get_value('尺寸'), input['尺寸'])
        check.equal(tablecheck1.get_value('箱型'), 'GP')
        check.equal(tablecheck1.get_value('箱高'), input['箱高'])
        check.equal(tablecheck1.get_value('持箱人'), input['持箱人'])
        check.equal(tablecheck1.get_value('直装'), 'Y')
        check.equal(tablecheck1.get_value('放行'), '未放')
        self.logger.info('装船箱放行：码头人工放行')
        self.click('xpath', "//span[contains(text(),'码头人工放行')]")
        tablecheck2 = Gtos_table(self.driver, 3)
        check.equal(tablecheck2.get_value('提单号'), boxnumber)
        self.click('xpath', "//i[@class='el-dialog__close el-icon el-icon-close']")
        check.equal(tablecheck.get_value('放行'), '放行')
        check.equal(tablecheck1.get_value('放行'), '放行')

    def search(self):
        Gtextinput = Gtos_text(self.driver)
        Gtextinput.search_select_by_label('出口船名航次', config.outportNumber)
        Gtextinput.input_by_label('箱号', config.outBoxNumber)
        self.logger.info('装船箱放行：查询航次、箱号')
        self.click('xpath', "//span[text()='检索']")

    def permitthrough(self):
        self.logger.info('装船箱放行：：码头人工放行')
        tablecheck = Gtos_table(self.driver)
        tablecheck.tick_off_box(1)
        tablecheck1 = Gtos_table(self.driver, 2)
        self.click('xpath', "//span[contains(text(),'码头人工放行')]")
        if tablecheck1.get_value('放行') == '放行':
            time.sleep(0.5)
            Tag(self.driver).closeTagGtos('装船箱放行')
        else:
            self.click('xpath', "//span[contains(text(),'码头人工放行')]")
            time.sleep(3)
            self.click('xpath', "//i[@class='el-dialog__close el-icon el-icon-close']")
            check.equal(tablecheck.get_value('放行'), '放行')
            check.equal(tablecheck1.get_value('放行'), '放行')
            time.sleep(0.5)
            Tag(self.driver).closeTagGtos('装船箱放行')
