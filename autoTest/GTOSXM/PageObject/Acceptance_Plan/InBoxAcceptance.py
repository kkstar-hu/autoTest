import time

import pytest_check as check
from Base.basepage import BasePage
from GTOSXM.Controls.text import Gtos_text
from GTOSXM.Config import config
from GTOSXM.Controls.Gtos_table import Gtos_table


class InBox_Acceptance(BasePage):
    """
    计划受理--安排计划--进箱受理
    """
    def choice_tree_straight(self,input):
        """
        选择计划类型
        """
        self.logger.info('计划：选择计划类型')
        self.click('xpath',f"//span[text()='{input['贸易类型']}']")

    def select_value(self):
        """
        选择进口船、提单号
        """
        self.logger.info('计划：输入航名航次')
        Gtextinput = Gtos_text(self.driver)
        Gtextinput.select_by_placeholder('请选择',config.outportNumber)

    def addPlan(self,input,boxnumber):
        """
        新增进场计划
        """
        try:
            self.logger.info('计划：新增进场计划箱')
            self.click('xpath',"(//span[text()='新增'])[1]")
            self.waitloading()
            Gtextinput = Gtos_text(self.driver)
            time.sleep(1)
            Gtextinput.input_by_label('箱号', boxnumber)
            Gtextinput.input_by_label('铅封号', 'A123')
            Gtextinput.select_by_label('尺寸', input['尺寸'])
            Gtextinput.select_by_label('箱型', input['箱型1'])
            Gtextinput.select_by_label('箱高', input['箱高'])
            Gtextinput.select_by_label('持箱人', input['持箱人'])
            Gtextinput.input_by_label('箱货总重', input['箱货总重'])
            Gtextinput.select_by_label('卸货港', input['卸货港'])
            Gtextinput.select_by_label_time('目的港', input['目的港'])
            self.save()
            self.check_alert('保存成功')
            tablecheck = Gtos_table(self.driver)
            self.logger.info('直装计划：校验字段')
            check.equal(tablecheck.get_value('箱号'), boxnumber)
            self.logger.info('本次直装箱号:'+ tablecheck.get_value('箱号')+'!!!!!!!!!!!!!!!!!')
            check.equal(tablecheck.get_value('贸易类型'), '内贸')
            check.equal(tablecheck.get_value('铅封号'), 'A123')
            check.equal(tablecheck.get_value('尺寸'), input['尺寸'])
            check.equal(tablecheck.get_value('箱型'), 'GP')
            check.equal(tablecheck.get_value('持箱人'), input['持箱人'])
            check.equal(tablecheck.get_value('箱高'), input['箱高'])
            check.equal(tablecheck.get_value('箱货总重'), input['箱货总重'])
            check.equal(tablecheck.get_value('卸货港'), input['卸货港'])
            check.equal(tablecheck.get_value('目的港'), input['目的港'])
        except:
            self.cancel()

    def Add_value(self,boxnumber):
        """
        新增货信息
        """
        try:
            self.logger.info('计划：新增货信息')
            self.click('xpath', "(//span[text()='新增'])[2]")
            time.sleep(1)
            Gtextinput = Gtos_text(self.driver)
            Gtextinput.input_by_label('提单号', boxnumber)
            Gtextinput.textarea_by_label('货名','石头')
            self.save()
            self.check_alert('保存成功')
            tablecheck = Gtos_table(self.driver,2)
            self.logger.info('直装计划：校验字段')
            check.equal(tablecheck.get_value('提单号'), boxnumber)
        except:
            self.cancel()

    def build_plan(self,input):
        """
        生产计划
        """
        self.logger.info('计划：生成计划')
        self.click('xpath',"//span[text()='生成计划']")
        Gtextinput = Gtos_text(self.driver)
        Gtextinput.select_by_label('申请人',input['申请人'])
        Gtextinput.select_by_label('流向/来源',input['流向/来源'])
        Gtextinput.element_wait_disappear("xpath","//div[@role='alert']//p")
        self.click('xpath',"//button/span[contains(text(),'保存')]")
        self.check_alert('计划保存成功')


