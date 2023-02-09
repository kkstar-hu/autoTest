import time

import pytest_check as check
from Base.basepage import BasePage
from Commons.Controls.table import Table
from Commons.Controls.text import text
from Commons.DateTime import DataTime
from NZYMS.Config import config


class Settlement_Charge(BasePage):
    """
    结算收费
    """
    def configuration(self):
        """
        配置收费
        """
        self.logger.info('查验计划收费：输入箱号、选择结算类型')
        textInput = text(self.driver)
        textInput.click('xpath', f'//span[text()="{config.showname}"]')
        textInput.click_by_index('xpath', "//span[text()='本地配置']", 1)
        textInput.input_by_label('金税盘号', '测试')
        textInput.click('xpath', "//div/button/span[contains(text(),'保存')]")
        self.waitloading()


    def out_pay(self,input):
        """
        出场收费
        """
        self.configuration()
        self.logger.info('查验计划收费：输入箱号、选择结算类型')
        textInput = text(self.driver)
        textInput.input_by_label('箱号', config.boxNumberOutPlan)
        textInput.select_by_placeholder('请选择结费点','10/出场计划')
        self.click("xpath", "//button//span[text()='检索']")
        self.waitloading()
        self.check_outplan_box_information(input)
        self.check_outplanbox(input)
        self.pay(input)
        self.refresh()






    def search(self,boxnumber,type,service_number=None,submit_number=None):
        textInput = text(self.driver)
        if service_number != None:
            textInput.input_by_label('业务号', service_number)
        if submit_number != None:
            textInput.input_by_label('报检编号', submit_number)
        textInput.input_by_label('箱号', boxnumber)
        textInput.select_by_label('结费类型', type)
        self.click("xpath", "//button//span[text()='检索']")
        self.waitloading()

    def pay(self,input):
        try:
            textInput = text(self.driver)
            self.click('xpath', "//span[text()='结费']")
            self.waitloading()
            self.element_wait("xpath", f"//form[@class='el-form']//label[contains(text(),'收款方式')]")
            if input["收款方式"] !=None:
                textInput.select_by_label('收款方式', input["收款方式"])
            if input["发票类型"] !=None:
                textInput.select_by_label('发票类型', input["发票类型"])
            textInput.click('xpath', f"//span[text()='{input['是否开票']}']")
            self.check_alert(input["chargeAlert"])
        except:
            self.refresh()
            self.cancel()

    def outPlanPay(self):
        self.click('xpath', "//button//span[contains(text(),'确定')]")


    def check_change_box_information(self,input):
        self.element_wait("xpath", "//div[text()='整改计划']")
        tableCheckfixed = Table(self.driver, 2)
        check.is_in(tableCheckfixed.get_value("整改作业类型"), input['整改类型'])
        check.equal(tableCheckfixed.get_value("整改结算主体"), input["结算主体"])
        tableCheck = Table(self.driver, 1)
        check.equal(tableCheck.get_value("箱号"), config.boxNumber)
        check.is_in(tableCheck.get_value("申请客户"), "上海永旭集装箱运输or上海禾旭货运代理")
        check.is_in(tableCheck.get_value("结算客户"), "上海永旭集装箱运输or上海禾旭货运代理")
        check.equal(tableCheck.get_value("备注"), input['备注'])
        check.is_in(tableCheck.get_value("是否关闭"), "否")
        check.equal(tableCheck.get_value("创建人"), config.createName)

    def check_check_plan_information(self, input):
        self.element_wait("xpath","//div[text()='查验计划']")
        tableCheckfixed = Table(self.driver, 2)
        check.equal(tableCheckfixed.get_value("计划类型"), input['计划类型'])
        tableCheck = Table(self.driver, 1)
        check.equal(tableCheck.get_value("计划状态"), "查验完成")
        check.equal(tableCheck.get_value("申请客户"), "上海永旭集装箱运输")
        check.equal(tableCheck.get_value("结算客户"), "上海永旭集装箱运输")
        check.equal(tableCheck.get_value("是否再生品"), input['是否再生品'])
        check.equal(tableCheck.get_value("是否放射性"), input['是否放射性'])
        check.equal(tableCheck.get_value("是否加急"), input['是否加急'])
        check.equal(tableCheck.get_value("是否熏蒸"), input['是否熏蒸'])
        check.is_in(tableCheck.get_value("查验科室"), input['查验科室'])
        check.equal(tableCheck.get_value("查验单位"), input['查验单位'])
        check.equal(tableCheck.get_value("备注"), input['备注'])
        check.equal(tableCheck.get_value("录入人"), config.createName)

    def check_checkbox(self, input):
        tableCheck = Table(self.driver, 4)
        check.equal(tableCheck.get_value("尺寸"), input['尺寸'])
        check.equal(tableCheck.get_value("箱型"), input['箱型'])
        check.equal(tableCheck.get_value("箱号"), config.boxNumber)
        check.equal(tableCheck.get_value("查验单位"), input['查验单位'])
        check.equal(tableCheck.get_value("查验计划状态"), "查验完成")
        check.equal(tableCheck.get_value("录入人"), config.createName)

    def check_outplanbox(self, input):
        tableCheck = Table(self.driver, 4)
        check.equal(tableCheck.get_value("尺寸"), input['尺寸'])
        check.is_in(tableCheck.get_value("箱型"), input['箱型'])
        check.equal(tableCheck.get_value("箱高"), input['箱高'])
        check.equal(tableCheck.get_value("箱号"), config.boxNumber)
        check.equal(tableCheck.get_value("空重标志"), input['空重'])
        check.is_in(tableCheck.get_value("持箱人"), input["持箱人"])

    def check_outplan_box_information(self,input):
        createTime = DataTime.GetTime()
        tableCheck = Table(self.driver, 2)
        check.equal(tableCheck.get_value("结算主体"), input["结算主体"])
        check.equal(tableCheck.get_value("计划号"), config.outplanNumber)
        check.is_in(tableCheck.get_value("出场作业类型"), input['出场作业类型'])
        tableCheck1 = Table(self.driver)
        check.is_in(tableCheck1.get_value("申请客户"), "上海永旭集装箱运输or上海禾旭货运代理")
        check.is_in(tableCheck1.get_value("结算客户"), "上海永旭集装箱运输or上海禾旭货运代理")
        check.is_in(tableCheck1.get_value("流向"), input['流向'])
        check.is_in(tableCheck1.get_value("去向地"), input['去向地'])
        check.equal(tableCheck1.get_value("备注"), input['备注'])
        check.is_in(tableCheck1.get_value("委托送港类型"), input['委托送港类型'])
        check.less(DataTime.get_dif_time(tableCheck1.get_value("创建时间"),createTime),300)
        check.equal(tableCheck1.get_value("创建人"), config.createName)