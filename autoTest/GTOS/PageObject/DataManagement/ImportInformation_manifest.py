import time

import pytest_check as check
from selenium.webdriver import Keys, ActionChains
from Base.basepage import BasePage
from Commons.Controls.text import text
from GTOS.Controls.text import Gtos_text
from GTOS.Config import config
from GTOS.Controls.Gtos_table import Gtos_table


class Manifest(BasePage):
    """
    进口资料
    """
    def AddManifest(self,input):
        """
        新增舱单
        """
        self.logger.info('步骤1：输入船名航次')
        Gtextinput = Gtos_text(self.driver)
        Gtextinput.input_noclear_placeholder_click('请输入关键词',input['进口船名航次'])
        self.logger.info('步骤2：检索')
        self.click('xpath',"//span[text()='检索']")
        try:
            if self.get_alert_text() == '未找到相关舱单信息':
                self.close_alert('未找到相关舱单信息')
            self.logger.info('步骤3：新增舱单货资料')
            self.click("xpath","(//div[@id='add'])[1]")
            time.sleep(1)
            textinput = Gtos_text(self.driver)
            textinput.input_by_label('提单号',config.boxNumber)
            textinput.select_by_label('卸货港',input['卸货港'])
            textinput.select_by_label('目的港',input['目的港'])
            self.logger.info('步骤4：保存，关闭新增页面')
            self.save()
            self.close()
            self.check_alert('新增成功')
            self.logger.info('步骤5：校验字段')
            row = self.rows_value()
            tablecheck = Gtos_table(self.driver)
            tablecheck.tick_off_box(row)
            em = self.get_element('xpath',f"//div[text()='{config.boxNumber}']")
            ActionChains(self.driver).move_to_element(em).click().perform()
            check.equal(tablecheck.get_value('提单号',row), config.boxNumber)
            check.equal(tablecheck.get_value('总箱数',row), '0')
            check.equal(tablecheck.get_value('卸货港',row), input['卸货港'])
            check.equal(tablecheck.get_value('目的港',row), input['目的港'])
        except:
            self.cancel()




    def AddBox(self,input):
        """
        新增舱单箱
        """
        try:
            self.logger.info('步骤1：新增舱单箱信息')
            textinput = Gtos_text(self.driver)
            self.click("xpath","(//div[@id='add'])[2]")
            textinput.input_by_label('箱号',config.boxNumber)
            textinput.select_by_label('尺寸',input['尺寸'])
            textinput.select_by_label('箱型','00')
            textinput.select_by_label('箱高',input['箱高'])
            textinput.select_by_label('箱状态',input['箱状态'])
            textinput.select_by_label('贸易类型',input['贸易类型'])
            textinput.select_by_label('持箱人',input['持箱人'])
            textinput.input_by_label('箱货总重',input['箱货总重'])
            self.logger.info('步骤2：保存，关闭新增页面')
            self.save()
            self.close()
            self.check_alert('新增成功')
            tablecheck1 = Gtos_table(self.driver)
            self.logger.info('步骤3：总箱数+1')
            check.equal(tablecheck1.get_value('总箱数'), '1')
        except:
            self.cancel()
        self.logger.info('步骤4：校验字段')
        tablecheck = Gtos_table(self.driver,2)
        check.equal(tablecheck.get_value('箱号'),config.boxNumber)
        check.equal(tablecheck.get_value('贸易类型'),input['贸易类型'])
        check.equal(tablecheck.get_value('尺寸'),input['尺寸'])
        check.equal(tablecheck.get_value('箱型'),input['箱型'])
        check.equal(tablecheck.get_value('箱高'),input['箱高'])
        check.equal(tablecheck.get_value('箱状态'),input['箱状态'])
        check.equal(tablecheck.get_value('持箱人'),input['持箱人'])
        check.equal(tablecheck.get_value('箱货总重'),input['箱货总重'])


    def choice_ship(self):
        """
        转船图箱-整船
        """
        self.logger.info('步骤1：转船图箱,整船')
        self.click('xpath',"//span[text()='转船图箱']")
        self.click('xpath',"//span[text()='整船']")
        self.click('xpath',"//span[contains(text(),'确定')]")
        self.check_alert('转船图成功')


    def choice_lading(self):
        """
        转船图箱-提单
        """
        self.logger.info('步骤1：转船图箱,整船')
        self.click('xpath',"//span[text()='转船图箱']")
        self.click('xpath',"//span[text()='提单']")



    def rows_name(self,index=1):
        """
        获取内容，用于check
        """
        pax_name = []
        att = []
        a = []
        # 通过标签名获取表格的所有行
        table_name = self.get_elements('xpath',f"(//div[@class='ag-header-row ag-header-row-column'])[{index}]//div[@class='ag-header-cell-label']//span[@ref='eText']")
        #  按行查询表格的数据，取出的数据是一整行，按,分隔每一列的数据
        for tr in table_name:
            # print(tr.text)     获取文本
            # print(tr.get_attribute('outerHTML'))   获取当前元素源代码
            # print(tr.is_displayed())      判断元素文本是不是被隐藏了
            # print(tr.get_attribute('attributeName'))
            # print(tr.get_attribute('textContent'))           获取隐藏的文本信息
            # print(tr.get_attribute('innerText'))          获取隐藏的文本信息
            att = (tr.get_attribute('textContent')).split("\n")
            pax_name.append(att)
        a = sum(pax_name,[])  #将 嵌套的列表合并成一个列表
        return a

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
        for y in a :
            if y == config.boxNumber:
                row = a[a.index(y)-1]
                return int(row)
        #return a  返回所有数据

    def table_information(self,name_index,value_index):
        a = self.rows_name(name_index)
        b = self.rows_value(value_index)
        c = dict(zip(a,b))
        return c