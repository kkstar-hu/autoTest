import time

import pytest_check as check
from selenium.webdriver import Keys, ActionChains
from Base.basepage import BasePage
from GTOSXM.Controls.text import Gtos_text
from GTOSXM.Config import config
from GTOSXM.Controls.Gtos_table import Gtos_table


class Manifest(BasePage):
    """
    进口资料
    """
    def AddManifest(self,input,boxnumber):
        """
        新增舱单
        """
        Gtextinput = Gtos_text(self.driver)
        Gtextinput.search_select_by_label('进口船名航次',config.importNumber)
        self.click('xpath',"//span[text()='检索']")
        try:
            if self.get_alert_text() == '未找到相关舱单信息':
                self.close_alert('未找到相关舱单信息')
            self.logger.info('舱单-新增舱单货资料'+boxnumber)
            self.click("xpath","(//div[@id='add'])[1]")
            time.sleep(1)
            textinput = Gtos_text(self.driver)
            textinput.input_by_label('提单号',boxnumber)
            textinput.select_by_label('装货港',input['装货港'])
            textinput.select_by_label('卸货港',input['卸货港'])
            textinput.select_by_label('目的港',input['目的港'])
            textinput.select_by_label('交货地',input['交货地'])
            textinput.select_by_label('货主',input['货主'])
            textinput.select_by_label('货代',input['货代'])
            textinput.select_by_label('运输方式',input['运输方式'])
            textinput.input_by_label('总件数', '1')
            textinput.input_by_label('总重量', '10000')
            textinput.input_by_label('总体积', '500')
            textinput.select_by_label('交付方式',input['交付方式'])
            textinput.select_by_label('货类',input['货类'])
            textinput.select_by_label('包装类型',input['包装类型'])
            textinput.input_by_label('货名', input['货名'])
            textinput.input_by_label('唛头', input['唛头'])
            textinput.input_by_label('发货人',input['发货人'])
            textinput.input_by_label('通知人', input['通知人'])
            self.save()
            self.close()
            self.check_alert('新增成功')
            self.logger.info('舱单-新增舱单后校验字段')
            row = self.rows_value(boxnumber)
            tablecheck = Gtos_table(self.driver)
            tablecheck.tick_off_box(row)
            em = self.get_element('xpath',f"//div[text()='{boxnumber}']")
            ActionChains(self.driver).move_to_element(em).click().perform()
            check.equal(tablecheck.get_value('提单号',row), boxnumber)
            self.logger.info('本次箱号:'+ tablecheck.get_value('提单号',row)+'!!!!!!!!!!!!!!!!!')
            check.equal(tablecheck.get_value('总箱数',row), '0')
            check.equal(tablecheck.get_value('货主',row), input['货主'])
            check.equal(tablecheck.get_value('货代',row), input['货代'])
            check.equal(tablecheck.get_value('装货港',row), input['装货港'])
            check.equal(tablecheck.get_value('卸货港',row), input['卸货港'])
            check.equal(tablecheck.get_value('目的港',row), input['目的港'])
            check.equal(tablecheck.get_value('交付方式',row), input['交付方式'])
            check.equal(tablecheck.get_value('货类',row), input['货类'])
            check.equal(tablecheck.get_value('货名',row), input['货名'])
            check.equal(tablecheck.get_value('唛头',row), input['唛头'])
            check.equal(tablecheck.get_value('发货人',row), input['发货人'])
            check.equal(tablecheck.get_value('通知人',row), input['通知人'])
            time.sleep(1)
            # check.equal(tablecheck.get_value('总件数',row), '1')
            # check.equal(tablecheck.get_value('总重量',row), '10000')
            # check.equal(tablecheck.get_value('总体积',row), '500')
        except:
            self.cancel()

    def AddBox(self,input,boxnumber):
        """
        新增舱单箱
        """
        try:
            self.logger.info('舱单-新增舱单箱信息'+boxnumber)
            textinput = Gtos_text(self.driver)
            self.click("xpath","(//div[@id='add'])[2]")
            time.sleep(0.5)
            textinput.input_by_label('箱号',boxnumber)
            textinput.select_by_label('尺寸',input['尺寸'])
            textinput.select_by_label('箱型','00')
            textinput.select_by_label('箱高',input['箱高'])
            textinput.select_by_label('箱状态',input['箱状态'])
            textinput.select_by_label('贸易类型',input['贸易类型'])
            textinput.input_by_label('铅封号','CBDS11')
            textinput.select_by_label('持箱人',input['持箱人'])
            textinput.input_by_label('箱货总重',input['箱货总重'])
            self.save()
            self.close()
            self.check_alert('新增成功')
            tablecheck1 = Gtos_table(self.driver)
            check.equal(tablecheck1.get_value('总箱数'), '1')
        except:
            self.cancel()
        self.logger.info('舱单-新增舱单箱保存后校验字段')
        tablecheck = Gtos_table(self.driver,2)
        check.equal(tablecheck.get_value('箱号'),boxnumber)
        check.equal(tablecheck.get_value('贸易类型'),input['贸易类型'])
        check.equal(tablecheck.get_value('铅封号'), 'CBDS11')
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
        self.logger.info('舱单-转船图箱,整船操作')
        self.click('xpath',"//span[text()='转船图箱']")
        self.click('xpath',"//span[text()='整船']")
        self.click('xpath',"//span[contains(text(),'确定')]")
        self.check_alert('转船图成功')


    def choice_lading(self):
        """
        转船图箱-提单
        """
        self.logger.info('舱单-转船图箱,提单操作')
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

    def rows_value(self,boxnumber,index=1):
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
            if y == boxnumber:
                row = a[a.index(y)-1]
                return int(row)
        #return a  返回所有数据

    def table_information(self,name_index,value_index):
        a = self.rows_name(name_index)
        b = self.rows_value(value_index)
        c = dict(zip(a,b))
        return c