import time

import pytest_check as check
from selenium.webdriver import ActionChains

from Base.basepage import BasePage
from GTOS.Controls.text import Gtos_text
from GTOS.Config import config
from GTOS.Controls.Gtos_table import Gtos_table

class NO_Structure_Monitoring(BasePage):
    """
    无结构船舶监控
    """
    def Retrieve(self,input):
        """
        输入内容，检索
        """
        self.logger.info('步骤1：输入航名航次')
        textinput = Gtos_text(self.driver)
        textinput.search_select_by_label('船名航次',config.outportNumber)
        self.logger.info('步骤2：检索')
        self.click('xpath',"//span[text()='检索']")

    def SendBox_check_values(self,input):
        """
        校验
        """
        self.logger.info('步骤3：校验内容')
        row = self.rows_value(3)
        tablecheck = Gtos_table(self.driver,3)
        check.is_in(tablecheck.get_value('箱号',row).replace(' ','').replace('\n',''),config.boxNumber)
        check.equal(tablecheck.get_value('卸货港',row), input['卸货港'])
        check.equal(tablecheck.get_value('作业状态',row), '可作业')
        check.equal(tablecheck.get_value('箱状态',row),input['箱状态'])
        check.equal(tablecheck.get_value('尺寸',row),input['尺寸'])
        check.equal(tablecheck.get_value('箱型',row),input['箱型'])
        check.equal(tablecheck.get_value('箱高',row),input['箱高'])
        check.equal(tablecheck.get_value('目的港',row),input['目的港'])
        check.equal(tablecheck.get_value('箱货总重(吨)',row),str(format(float(input['箱货总重']) * float(0.001),'.3f')))
        check.equal(tablecheck.get_value('持箱人',row),input['持箱人'])


    def Send_Box(self,input):
        """
        发箱
        """
        self.Retrieve(input)
        self.SendBox_check_values(input)
        self.logger.info('步骤1：勾选后发箱')
        row = self.rows_value(3)
        tablecheck = Gtos_table(self.driver, 3)
        tablecheck.tick_off_box(row)
        self.click('xpath',"//span[text()='发箱']")
        self.check_alert('发箱成功')
        self.logger.info('步骤2：校验内容')
        check.equal(tablecheck.get_value('作业状态',row), '等待作业')

    def LadeShip_Send_Box(self):
        """
        发箱
        """

        self.logger.info('步骤1：勾选后发箱')
        table = Gtos_table(self.driver,4)
        table.check2("箱号", config.boxNumber)
        self.click('id',"shipmentconfirm")
        self.check_alert('发箱成功')
        self.logger.info('步骤2：校验内容')
        rowid = table.select_row("箱号", config.boxNumber)
        check.equal(table.get_value_by_rowid(rowid,'作业状态'), '等待作业')

    def clickLadeShipTag(self):
        self.click("xpath", "//div[@class='panel-header__left']//div[text()=' 装船 ']")
    def LadeShip_check_values(self,input):
        """
        校验
        """
        self.logger.info('步骤3：校验内容')
        tablecheck = Gtos_table(self.driver,4)
        rowid = tablecheck.select_row2("箱号", config.boxNumber)
        check.equal(tablecheck.get_value_by_rowid(rowid, '尺寸'), input['尺寸'])
        check.equal(tablecheck.get_value_by_rowid(rowid, '箱型'), input['箱型'])
        check.equal(tablecheck.get_value_by_rowid(rowid, '箱高'), input['箱高'])
        check.equal(tablecheck.get_value_by_rowid(rowid, '持箱人'), input['持箱人'])
        check.equal(tablecheck.get_value_by_rowid(rowid, '箱货总重(吨)'), input['箱货总重check'])
        check.equal(tablecheck.get_value_by_rowid(rowid, '卸货港'), input['卸货港'])
        check.equal(tablecheck.get_value_by_rowid(rowid, '目的港'), input['目的港'])
        check.equal(tablecheck.get_value_by_rowid(rowid, '作业状态'), '提交作业')

    def choice_loading(self,input):
        """
        选择直装
        """
        self.Retrieve(input)
        self.click('xpath',"//div[contains(text(),'直装')]")
        self.logger.info('步骤1：勾选数据')
        row = self.rows_value(6)
        tablecheck = Gtos_table(self.driver, 6)
        tablecheck.tick_off_box(row)
        self.logger.info('步骤2：校验数据')
        check.is_in(tablecheck.get_value('箱号',row),config.boxNumber)
        check.equal(tablecheck.get_value('报道',row),'Y')
        check.equal(tablecheck.get_value('集卡',row),input['车牌']+input['集卡编号'])
        check.equal(tablecheck.get_value('作业状态',row), '提交作业')
        check.equal(tablecheck.get_value('尺寸',row),input['尺寸'])
        check.equal(tablecheck.get_value('箱型',row),input['箱型'])
        check.equal(tablecheck.get_value('冷箱',row),'N')
        check.equal(tablecheck.get_value('提单号',row),config.boxNumber)
        check.equal(tablecheck.get_value('箱货总重(吨)',row),str(format(float(input['箱货总重']) * float(0.001),'.3f')))
        self.logger.info('步骤3：允许直装')
        self.click('xpath', "(//span[contains(text(),'允许直装')])[1]")
        self.check_alert('操作成功')
        check.equal(tablecheck.get_value('作业状态',row), '等待作业')


    def choice_lifting(self,input):
        """
        选择直提
        """
        self.Retrieve(input)
        self.click('xpath',"//div[contains(text(),'直提')]")
        self.logger.info('步骤1：勾选数据')
        row = self.rows_value(5)
        tablecheck = Gtos_table(self.driver, 5)
        tablecheck.tick_off_box(row)
        self.logger.info('步骤2：校验数据')
        check.is_in(tablecheck.get_value('箱号',row),config.boxNumber)
        check.equal(tablecheck.get_value('报道',row),'Y')
        check.equal(tablecheck.get_value('集卡',row),input['车牌']+input['集卡编号'])
        check.equal(tablecheck.get_value('作业状态',row), '可作业')
        check.equal(tablecheck.get_value('尺寸',row),input['尺寸'])
        check.equal(tablecheck.get_value('箱型',row),input['箱型'])
        check.equal(tablecheck.get_value('冷箱',row),'N')
        check.equal(tablecheck.get_value('提单号',row),config.boxNumber)
        check.equal(tablecheck.get_value('箱货总重(吨)',row),str(format(float(input['箱货总重']) * float(0.001),'.3f')))
        self.logger.info('步骤3：允许直装')
        self.click('xpath', "(//span[contains(text(),'允许直提')])[1]")
        self.check_alert('操作成功')
        check.equal(tablecheck.get_value('作业状态',row), '等待作业')

    def ship_operation(self,input):
        """
        靠泊，桥吊操作
        """
        self.Retrieve(input)
        self.logger.info('步骤3：校验字段')
        tablecheck = Gtos_table(self.driver)
        check.equal(tablecheck.get_value('靠泊状态'),'未靠')
        self.logger.info('步骤4：靠泊确认')
        self.click('x',"//span[text()='靠泊确认']")
        self.click('x',"//input[@placeholder='靠泊时间']")
        self.click('x',"//span[contains(text(),'此刻')]")
        self.click('x',"//span[text()='提交']")
        self.check_alert('提交成功')
        self.close_alert('提交成功')
        check.equal(tablecheck.get_value('靠泊状态'),'靠泊')
        self.logger.info('步骤5：分配桥吊')
        self.click('x',"//span[text()='添加桥吊']")
        em = self.get_element('x',"(//div[@class='grid'])[1]//span[text()='导入']")
        ActionChains(self.driver).move_to_element(em).click().perform()
        self.check_alert('保存成功')
        self.close_alert('保存成功')
        tablecheck1 = Gtos_table(self.driver,2)
        check.equal(tablecheck1.get_value('状态'),'计划')
        self.click('x',"//i[@class='el-dialog__close el-icon el-icon-close']")
        self.logger.info('步骤6：桥吊开工')
        self.click('x',"//span[text()='桥吊开工']")
        self.check_alert('操作成功')
        check.equal(tablecheck1.get_value('状态'),'开工')



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
        #  按行查询表格的数据，取出的数据是一整行，按,分隔每一列的数据
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
        if index == 3 :
            for y in a :
                if y == '可作业':
                    row = a[a.index(y)-9]
                    return int(row)
        if index == 6 or index == 5 :
            for y in a:
                if y == config.boxNumber:
                    row = a[a.index(y)-1]
                    return int(row)
