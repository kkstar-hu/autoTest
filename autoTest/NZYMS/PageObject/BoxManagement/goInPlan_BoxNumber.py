import time
from Base.basepage import BasePage
from Commons.Controls.text import text
from Commons.Controls.table import Table
from Commons.DateTime import DataTime
from NZYMS.config import config
import pytest_check as check


class GoInPlan_BoxNumber(BasePage):

    def addPlan(self,input):
        try:
            self.logger.info('进箱计划：添加主计划')
            self.element_wait("xpath","(//div[@id='add'])[1]")
            self.click("xpath","(//div[@id='add'])[1]")
            if input["堆场"]!=None:
                self.get_elements("xpath","//form[@class='el-form']//label[contains(text(),'堆场')]//following-sibling::div//input")[1].click()
                self.get_elements("xpath","//div[@class='el-scrollbar']//span[@title='"+input["堆场"]+"']")[1].click()
            if input["进场作业类型"] != None:
                self.get_elements("xpath","//form[@class='el-form']//label[contains(text(),'进场作业类型')]//following-sibling::div//input")[1].click()
                self.get_elements("xpath", "//div[@class='el-scrollbar']//span[@title='" + input["进场作业类型"] + "']")[1].click()
            textInput=text(self.driver)
            self.logger.info('check1：验证计划号可否编辑')
            check.is_false(textInput.text_isenable("计划号"))
            textInput.special_input("申请客户","SHA","SHAPGJHWYS/上海永旭集装箱运输")
            textInput.special_input("结算客户", "SHA", "SHAPGJHWYS/上海永旭集装箱运输")
            if input["送港类型"] != None:
                textInput.select_by_label("送港类型",input['送港类型'])
            if input["外部编号"] != None:
                textInput.input_by_number("外部编号", input['外部编号'])
            if input["计划来源"] != None:
                textInput.select_by_index("计划来源", input['计划来源'])
            if input["来源地"] != None:
                textInput.select_by_label("来源地", input['来源地'])
            if input["备注"] != None:
                textInput.textarea_by_label("备注", input['备注'])
            self.save_and_close()
            createTime = DataTime.GetTime()
            self.logger.info('check2：验证添加主计划弹出提示信息')
            self.check_alert(input["addplanalert"])
        except:
            self.cancel()
        if input["addplanalert"]=='新增成功':
            tableCheckfixed=Table(self.driver,2)
            self.logger.info('check3：验证添加后列表的值正确')
            config.planNumber=tableCheckfixed.get_value("计划号")
            check.is_in(tableCheckfixed.get_value("进场作业类型"),input['进场作业类型'])
            tableCheck = Table(self.driver)
            check.is_in(tableCheck.get_value("堆场"), input['堆场'])
            check.equal(tableCheck.get_value("计划状态"), "计划")
            check.equal(tableCheck.get_value("申请客户"), "上海永旭集装箱运输")
            check.equal(tableCheck.get_value("结算客户"), "上海永旭集装箱运输")
            check.is_in(tableCheck.get_value("计划来源"), input['计划来源'])
            check.is_in(tableCheck.get_value("来源地"), input['来源地'])
            check.equal(tableCheck.get_value("送港类型"), input['送港类型'])
            check.equal(tableCheck.get_value("外部编号"), input['外部编号'])
            check.equal(tableCheck.get_value("是否安排运务"), input['是否安排运务'])
            check.equal(tableCheck.get_value("备注"), input['备注'])
            check.less(DataTime.get_dif_time(createTime,tableCheck.get_value("创建时间")),100)
            check.equal(tableCheck.get_value("创建人"), config.createName)

    def addBoxPlan(self,input,boxNumber):
        try:
            self.logger.info('进箱计划：添加计划箱')
            self.element_wait("xpath", "(//div[@id='add'])[2]")
            self.click("xpath","(//div[@id='add'])[2]")
            textInput = text(self.driver)
            textInput.input_by_number("箱号",boxNumber)
            if input["尺寸"] != None:
                textInput.select_by_label("尺寸",input['尺寸'])
            if input["箱型"] != None:
                textInput.select_by_label("箱型",input['箱型'])
            if input["箱高"] != None:
                textInput.select_by_label("箱高",input["箱高"])
            if input["持箱人"] != None:
                textInput.select_by_label("持箱人",input['持箱人'])
            self.save_and_close()
            time.sleep(0.3)
        except:
            self.click("x","//button//span[text()='取消 ']")
        self.check_alert(input["addplanalert"])
        tableCheckfixed = Table(self.driver,5)
        check.equal(tableCheckfixed.get_value("箱号"), boxNumber)
        self.logger.info('添加箱号为：'+tableCheckfixed.get_value("箱号"))
        print('添加箱号为：'+tableCheckfixed.get_value("箱号"))
        tableCheck = Table(self.driver, 4)
        check.equal(tableCheck.get_value("尺寸"), input['尺寸'])
        check.is_in(tableCheck.get_value("持箱人"), input['持箱人'])
        check.equal(tableCheck.get_value("箱高"), input['箱高'])
        check.equal(tableCheck.get_value("箱型"), input['箱型'])

    def addBoxInformation(self, input):
        try:
            self.logger.info('进箱计划：添加箱货信息')
            self.element_wait("xpath", "(//div[@id='add'])[3]")
            self.click("xpath", "(//div[@id='add'])[3]")
            textInput = text(self.driver)
            if input["提单号"] != None:
                textInput.input_by_label("提单号", input['提单号'])
            if input["件数"] != None:
                textInput.input_by_label("件数", input['件数'])
            if input["重量"] != None:
                textInput.input_by_label("重量", input['重量'])
            if input["货名"] != None:
                textInput.input_by_label("货名", input['货名'])
            self.save_and_close()
        except:
            self.cancel()
        self.check_alert(input["addplanalert"])
        tableCheck = Table(self.driver,7)
        check.equal(tableCheck.get_value("提单号"), input['提单号'])

    def clickExcute(self,row):
        table= Table(self.driver, 3)
        table.excuteButton(row)
        self.click("xpath","//div[@class='el-message-box__btns']//span[contains(text(),'确定')]")
        check.is_true(self.has_alert("下发执行成功"))
        tableCheck = Table(self.driver)
        self.logger.info('check3：验证执行按钮后计划状态变执行状态')
        check.equal(tableCheck.get_value("计划状态"), "执行")
