import time
import pytest_check as check
from Base.basepage import BasePage
from GTOS.Config.config import takeNumber
from GTOS.Controls.text import Gtos_text
from GTOS.Config import config
from GTOS.Controls.Gtos_table import Gtos_table

class No_Structure_Stowage(BasePage):
    """
    无结构船舶配载
    """
    def search(self):
        self.logger.info('步骤1：输入船名航次')
        Gtextinput = Gtos_text(self.driver)
        Gtextinput.search_select_by_label('出口船名航次', config.outportNumber)
        self.logger.info('步骤2：检索')
        self.click('xpath', "//span[text()='检索']")

    def check(self,input,boxNumber,TDNumber=None):
        tablecheck = Gtos_table(self.driver)
        rowid=tablecheck.select_row("箱号",boxNumber)
        check.equal(tablecheck.get_value_by_rowid(rowid,'配载'), '未配')
        check.equal(tablecheck.get_value_by_rowid(rowid,'放行'), '放行')
        check.equal(tablecheck.get_value_by_rowid(rowid,'尺寸'), input['尺寸'])
        check.equal(tablecheck.get_value_by_rowid(rowid,'箱型'), input['箱型'])
        check.equal(tablecheck.get_value_by_rowid(rowid,'箱高'), input['箱高'])
        check.equal(tablecheck.get_value_by_rowid(rowid,'持箱人'), input['持箱人'])
        check.equal(tablecheck.get_value_by_rowid(rowid,'箱货总重'), input['箱货总重'])
        check.equal(tablecheck.get_value_by_rowid(rowid,'卸货港'), input['卸货港'])
        check.equal(tablecheck.get_value_by_rowid(rowid,'目的港'), input['目的港'])
        if TDNumber!=None:
            check.equal(tablecheck.get_value_by_rowid(rowid, '提单号'),TDNumber)
        check.equal(tablecheck.get_value_by_rowid(rowid,'作业状态'), '可作业')
    def stowage(self,boxNumber):
        table = Gtos_table(self.driver)
        table.check("箱号",boxNumber)
        self.click('xpath', "//span[contains(text(),'保存配载')]")
        self.check_alert('配载成功')
        rowid=table.select_row("箱号",boxNumber)
        check.equal(table.get_value_by_rowid(rowid,'配载'), '已配')
        check.equal(table.get_value_by_rowid(rowid,'作业状态'), '提交作业')

