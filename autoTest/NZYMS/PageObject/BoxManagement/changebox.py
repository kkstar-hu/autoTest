from Base.basepage import BasePage
from Commons.Controls.text import text
from Commons.Controls.table import Table
from Commons.DateTime import DataTime
from NZYMS.config import config
import pytest_check as check


class ChangeBox(BasePage):

    def search(self,input):
        textInput = text(self.driver)
        self.click("xpath","//button//span[contains(text(),'更多')]")
        textInput.input_by_label("箱号", config.boxNumber)
        textInput.select_by_label("堆场", input["堆场"])
        textInput.select_by_label("整改结算主体", input["整改结算主体"])
        self.click("xpath","//button//span[text()='检索']")

    def checkboxInformation(self, input):
        tablecheckfixed = Table(self.driver, 2)
        check.equal(tablecheckfixed.get_value("箱号"), config.boxNumber)
        check.equal(tablecheckfixed.get_value("整改结算主体"), input["结算主体"])
        check.equal(tablecheckfixed.get_value("进场作业类型"), input["进场作业类型"])
        tablecheck = Table(self.driver, 1)
        check.equal(tablecheck.get_value("持箱人"), input["持箱人"])
        check.equal(tablecheck.get_value("尺寸箱型"), input["尺寸箱型"])
        check.equal(tablecheck.get_value("箱高"), input["箱高"])



    def addchangePlan(self, input):
        try:
            self.logger.info('集装箱整改：添加计划箱')
            self.click("xpath", "//div[@id='add']")
            textInput = text(self.driver)
            check.is_false(textInput.text_isenable("整改单号",index=0))
            check.is_false(textInput.text_isenable("箱号"))
            textInput.special_input("申请客户", "SHA", "SHAPGJHWYS/上海永旭集装箱运输")
            textInput.special_input("结算客户", "SHA", "SHAPGJHWYS/上海永旭集装箱运输")
            if input["整改类型"] != None:
                textInput.select_by_label("整改类型", input['整改类型'])
            if input["报检编号"] != None:
                textInput.input_by_label("报检编号", input['报检编号'])
            if input["备注"] != None:
                textInput.textarea_by_label("备注", input['备注'])
            self.save_and_close()
            self.check_alert(input["alert"])
        except:
            self.cancel()
        createTime = DataTime.GetTime()
        if input["alert"]=="新增成功":
            tableCheckfixed = Table(self.driver, 5)
            config.changeNumber = tableCheckfixed.get_value("整改单号")
            check.equal(tableCheckfixed.get_value("箱号"), config.boxNumber)
            check.is_in(tableCheckfixed.get_value("整改作业类型"), input['整改类型'])
            tableCheck = Table(self.driver, 4)
            check.equal(tableCheck.get_value("申请客户"),"上海永旭集装箱运输")
            check.is_in(tableCheck.get_value("结算客户"),"上海永旭集装箱运输")
            check.equal(tableCheck.get_value("备注"), input['备注'])
            check.is_in(tableCheck.get_value("是否关闭"), "否")
            check.less(DataTime.get_dif_time(createTime,tableCheck.get_value("创建时间")), 100)
            check.equal(tableCheck.get_value("创建人"), config.createName)
