import time
import pytest_check as check
from Base.basepage import BasePage
from Commons.Controls.el_table import ELtable
from Commons.Controls.table import Table
from Commons.Controls.text import text
from Commons.DateTime import DataTime
from NZYMS.config import config
from Commons.menu import Menu
from Commons.Controls.tag import Tag
from NZYMS.PageObject.PayManagement.Settlement_charge import Settlement_Charge

class Out_Plan(BasePage):
    """出场计划"""
    def addPlan(self, input):
        try:
            self.logger.info('出场计划：添加主计划')
            self.click('xpath',"//div[@id='add']")
            self.waitloading()
            textInput = text(self.driver)
            self.logger.info('出场计划：输入内容')
            textInput.select_by_index('堆场', input['堆场'],1)
            if input['出场作业类型'] is not None:
                textInput.select_by_index('出场作业类型',input['出场作业类型'],1)
            self.logger.info('check1：验证计划号可否编辑')
            check.is_false(textInput.text_isenable("计划号"))
            textInput.special_input("申请客户","SHA","SHAPGJHWYS/上海永旭集装箱运输")
            textInput.special_input("结算客户", "SHA", "SHAPGJHWYS/上海永旭集装箱运输")
            if input["委托送港类型"] != None:
                textInput.select_by_label("委托送港类型",input['委托送港类型'])
            if input["流向"] != None:
                textInput.select_by_label("流向", input['流向'])
            if input["去向地"] != None:
                textInput.select_by_label("去向地", input['去向地'])
            if input["备注"] != None:
                textInput.textarea_by_label("备注", input['备注'])
            self.save_and_close()
        except:
            self.cancel()
        createTime = DataTime.GetTime()
        self.logger.info('check1：验证添加主计划弹出提示信息')
        self.check_alert(input["addplanalert"])
        tableCheck=Table(self.driver,2)
        self.logger.info('check2：验证添加后列表的值正确')
        config.outplanNumber=tableCheck.get_value("计划号")
        self.logger.info("出库计划号:" + config.outplanNumber)
        check.is_in(tableCheck.get_value("出场作业类型"),input['出场作业类型'])
        tableCheck1=Table(self.driver)
        check.is_in(tableCheck1.get_value("堆场"),input['堆场'])
        check.equal(tableCheck1.get_value("计划状态"), "计划")
        check.is_in(tableCheck1.get_value("申请客户"), "上海永旭集装箱运输or上海禾旭货运代理")
        check.is_in(tableCheck1.get_value("结算客户"), "上海永旭集装箱运输or上海禾旭货运代理")
        check.is_in(tableCheck1.get_value("流向"), input['流向'])
        check.is_in(tableCheck1.get_value("去向地"), input['去向地'])
        check.equal(tableCheck1.get_value("备注"), input['备注'])
        check.is_in(tableCheck1.get_value("委托送港类型"), input['委托送港类型'])
        check.less(DataTime.get_dif_time(createTime,tableCheck1.get_value("创建时间")),100)
        check.equal(tableCheck1.get_value("创建人"), config.createName)

    def addBoxPlan(self,input):
        """新增计划箱"""
        self.logger.info('出场计划：添加计划箱')
        self.click_by_index('xpath',"//div[@id='add']",1)
        self.waitloading()
        textInput = text(self.driver)
        textInput.get_elements('xpath', f'//input[@placeholder="请选择"]')[4].click()
        textInput.get_elements('xpath', f"//div[@class='el-scrollbar']//span[text()='{input['堆场']}']")[1].click()
        textInput.input_by_placeholder("请输入箱号", config.boxNumber)
        self.click_by_index("xpath", "(//button//span[text()='检索'])",1)
        tableCheck = ELtable(self.driver)
        self.logger.info('check1：验证添加作业指令窗口中列表的值正确')
        check.is_in(tableCheck.get_value_by_trElement("箱号", config.boxNumberOutPlan, "堆场"), input['堆场'])
        check.equal(tableCheck.get_value_by_trElement("箱号", config.boxNumberOutPlan, "尺寸"), input['尺寸'])
        check.is_in(tableCheck.get_value_by_trElement("箱号", config.boxNumberOutPlan, "箱型"), input['箱型'])
        check.equal(tableCheck.get_value_by_trElement("箱号", config.boxNumberOutPlan, "箱高"), input['箱高'])
        check.equal(tableCheck.get_value_by_trElement("箱号", config.boxNumberOutPlan, "进场作业类型"), input['进场作业类型'])
        tableCheck.select_row("箱号", config.boxNumber)
        self.click("xpath","//button//span[contains(text(),'确认')]")

    def pay_for_box(self,input):
        """
        新增计划箱后付款
        """
        textInput = text(self.driver)
        tableCheck = Table(self.driver)
        self.logger.info('出场计划：付款')
        value_text = self.get_alert_text()
        print(value_text)
        if self.elementExist("xpath", f"//form[@class='el-form']//label[contains(text(),'收款方式')]") is True:
            if input['收款方式'] is not None:
                textInput.select_by_label('收款方式',input['收款方式'])
            if input['发票类型'] is not None:
                textInput.select_by_label('发票类型',input['发票类型'])
            textInput.click('xpath',f"//span[text()='{input['是否开票']}']")
            self.logger.info('check3：仅开票后自动执行，计划内搜不到')
        elif self.elementExist('xpath',"//p[text()='当前为月结，是否继续?']") is True:
            self.click('xpath',"//button//span[contains(text(),'确定')]")
            self.logger.info('check1：月票确定后自动执行，计划状态变执行状态')
            time.sleep(1)
            check.equal(tableCheck.get_value("计划状态"), "执行")
        elif value_text == f'箱号[{config.boxNumber}]为转栈箱且未输入出码头时间！':
            self.logger.info('出场计划：设置出场码头时间')
            textInput.click('xpath',"//div[@class='toscom-buttongroup']//div[@id='time']")
            textInput.click('xpath',"//div[@class='vxe-modal--box']//input[@placeholder='选择日期时间']")
            textInput.click('xpath',"//button[@class='el-button el-picker-panel__link-btn el-button--default el-button--mini is-plain']")
            textInput.click('xpath',"//div[@class='vxe-modal--footer']//span[contains(text(),'确认')]")
            self.clk()
            Tag(self.driver).closeTag("出场计划")
            menu = Menu(self.driver)
            menu.select_level_Menu("费收管理,费用管理,结算收费")
            se_charge = Settlement_Charge(self.driver)
            se_charge.out_pay(input)
            Tag(self.driver).closeTag("结算收费")

    def choice_plan(self,input):
        """
        选择主计划
        """
        tableCheck=Table(self.driver)
        textInput = text(self.driver)
        textInput.click_by_index('xpath','//input[@placeholder="请选择"]',1)
        textInput.click('xpath',f"//span[text()='{input['结算主体']}']")
        textInput.click_by_index('xpath','//input[@placeholder="请选择"]',2)
        textInput.click('xpath',f"//span[text()='{input['计划状态']}']")
        self.click('xpath',"//span[text()='检索']")

    def clk(self,row=1):
        table= Table(self.driver,3)
        table.excuteButton(row)
        self.click("xpath","//div[@class='el-message-box__btns']//span[contains(text(),'确定')]")
        self.waitloading()
        tableCheck=Table(self.driver)
        self.logger.info('check3：验证执行按钮后计划状态变执行状态')
        check.equal(tableCheck.get_value("计划状态"), "执行")

