import time
import pytest_check as check
from Base.basepage import BasePage
from GTOS.Controls.text import Gtos_text
from GTOS.Config import config
from GTOS.Controls.Gtos_table import Gtos_table

class No_Structure_Stowage(BasePage):
    """
    无结构船舶配载
    """
    def Retrieve(self,input):
        """
        输入船名航次
        """
        self.logger.info('步骤1：输入船名航次')
        Gtextinput = Gtos_text(self.driver)
        # Gtextinput.input_noclear_placeholder_click('请输入关键词', input['出口船名航次'])
        Gtextinput.search_select_by_label('出口船名航次', config.outportNumber)
        self.logger.info('步骤2：检索')
        self.click('xpath',"//span[text()='检索']")
        self.logger.info('步骤3：校验内容')
        tablecheck = Gtos_table(self.driver)
        row = self.rows_value()
        tablecheck.tick_off_box(row)
        check.equal(tablecheck.get_value('配载',row), '未配')
        check.equal(tablecheck.get_value('放行',row), '放行')
        check.equal(tablecheck.get_value('箱号',row), config.boxNumber)
        check.equal(tablecheck.get_value('尺寸',row),input['尺寸'])
        check.equal(tablecheck.get_value('箱型',row),input['箱型'])
        check.equal(tablecheck.get_value('箱高',row),input['箱高'])
        check.equal(tablecheck.get_value('持箱人',row),input['持箱人'])
        check.equal(tablecheck.get_value('箱货总重',row),input['箱货总重'])
        check.equal(tablecheck.get_value('卸货港',row), input['卸货港'])
        check.equal(tablecheck.get_value('目的港',row), input['目的港'])
        check.equal(tablecheck.get_value('作业状态',row), '可作业')
        self.logger.info('步骤4：保存配载')
        self.click('xpath',"//span[contains(text(),'保存配载')]")
        self.check_alert('配载成功')
        check.equal(tablecheck.get_value('配载',row), '已配')
        check.equal(tablecheck.get_value('作业状态',row), '提交作业')


    def search(self,input):
        self.logger.info('步骤1：输入船名航次')
        Gtextinput = Gtos_text(self.driver)
        Gtextinput.search_select_by_label('出口船名航次', input['出口船名航次'])
        self.logger.info('步骤2：检索')
        self.click('xpath', "//span[text()='检索']")

    def check(self,input):
        tablecheck = Gtos_table(self.driver)
        rowid=tablecheck.select_row("箱号",config.boxNumber)
        check.equal(tablecheck.get_value_by_rowid(rowid,'配载'), '未配')
        check.equal(tablecheck.get_value_by_rowid(rowid,'放行'), '放行')
        check.equal(tablecheck.get_value_by_rowid(rowid,'箱号'), config.boxNumber)
        check.equal(tablecheck.get_value_by_rowid(rowid,'尺寸'), input['尺寸'])
        check.equal(tablecheck.get_value_by_rowid(rowid,'箱型'), input['箱型'])
        check.equal(tablecheck.get_value_by_rowid(rowid,'箱高'), input['箱高'])
        check.equal(tablecheck.get_value_by_rowid(rowid,'持箱人'), input['持箱人'])
        check.equal(tablecheck.get_value_by_rowid(rowid,'箱货总重'), input['箱货总重'])
        check.equal(tablecheck.get_value_by_rowid(rowid,'卸货港'), input['卸货港'])
        check.equal(tablecheck.get_value_by_rowid(rowid,'目的港'), input['目的港'])
        check.equal(tablecheck.get_value_by_rowid(rowid, '提单号'),config.takeNumber)
        check.equal(tablecheck.get_value_by_rowid(rowid,'作业状态'), '可作业')
    def stowage(self):
        table = Gtos_table(self.driver)
        table.check("箱号",config.boxNumber)
        self.click('xpath', "//span[contains(text(),'保存配载')]")
        self.check_alert('配载成功')
        rowid=table.select_row("箱号",config.boxNumber)
        check.equal(table.get_value_by_rowid(rowid,'配载'), '已配')
        check.equal(table.get_value_by_rowid(rowid,'作业状态'), '提交作业')


    def rows_value(self,index=1):
        """
        获取内容，用于check
        """
        pax_value = []
        att = []
        a = []
        b= []
        # 通过标签名获取表格的所有行
        table_value = self.get_elements('xpath',f"(//div[@class='ag-center-cols-viewport'])[{index}]//div[@role='gridcell']")
        for tr in table_value:
            # print(tr.text)     获取文本
            # print(tr.get_attribute('outerHTML'))   获取当前元素源代码
            # print(tr.is_displayed())      判断元素文本是不是被隐藏了
            # print(tr.get_attribute('attributeName'))
            # print(tr.get_attribute('textContent'))           获取隐藏的文本信息
            # print(tr.get_attribute('innerText'))          获取隐藏的文本信息
            att = (tr.get_attribute('textContent')).split("\n")
            pax_value.append(att)
        for i in pax_value:
            if len(i) == 1:
                b.append(i)
                a = sum(b,[])
        for y in a :
            if y == '未配':
                row = a[a.index(y)-1]
                return int(row)
