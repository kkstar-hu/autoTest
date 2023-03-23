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
            time.sleep(1)
            self.save()
            self.close()
            self.check_alert('新增成功')
            self.logger.info('舱单-新增舱单后校验字段')
            tablecheck = Gtos_table(self.driver)
            tablecheck.check('提单号',boxnumber)
            rowid = tablecheck.select_row('提单号', boxnumber)
            self.logger.info('本次箱号:'+ tablecheck.get_value_by_rowid(rowid,'提单号')+'!!!!!!!!!!!!!!!!!')
            check.equal(tablecheck.get_value_by_rowid(rowid,'总箱数'), '0')
            check.equal(tablecheck.get_value_by_rowid(rowid,'货主'), input['货主'])
            check.equal(tablecheck.get_value_by_rowid(rowid,'货代'), input['货代'])
            check.equal(tablecheck.get_value_by_rowid(rowid,'装货港'), input['装货港'])
            check.equal(tablecheck.get_value_by_rowid(rowid,'卸货港'), input['卸货港'])
            check.equal(tablecheck.get_value_by_rowid(rowid,'目的港'), input['目的港'])
            check.equal(tablecheck.get_value_by_rowid(rowid,'交付方式'), input['交付方式'])
            check.equal(tablecheck.get_value_by_rowid(rowid,'货类'), input['货类'])
            check.equal(tablecheck.get_value_by_rowid(rowid,'货名'), input['货名'])
            check.equal(tablecheck.get_value_by_rowid(rowid,'唛头'), input['唛头'])
            check.equal(tablecheck.get_value_by_rowid(rowid,'发货人'), input['发货人'])
            check.equal(tablecheck.get_value_by_rowid(rowid,'通知人'), input['通知人'])
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
            time.sleep(1)
            textinput.input_by_label('箱号',boxnumber)
            textinput.select_by_label('尺寸',input['尺寸'])
            textinput.select_by_label('箱型','00')
            textinput.select_by_label('箱高',input['箱高'])
            textinput.select_by_label('箱状态',input['箱状态'])
            textinput.select_by_label('贸易类型',input['贸易类型'])
            textinput.input_by_label('铅封号','CBDS11')
            textinput.select_by_label('持箱人',input['持箱人'])
            textinput.input_by_label('箱货总重',input['箱货总重'])
            time.sleep(1)
            self.save()
            time.sleep(1)
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
        time.sleep(1)
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

