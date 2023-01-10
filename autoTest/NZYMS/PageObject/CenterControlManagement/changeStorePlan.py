from Base.basepage import BasePage
from Commons.Controls.text import text
from Commons.Controls.table import Table
from Commons.Controls.el_table import ELtable
from NZYMS.Config import config
import pytest_check as check
from Commons.DateTime import DataTime


class ChangeStorePlan(BasePage):

    def addChangePlan(self,input,boxNumber):
        try:
            self.logger.info('步骤1：添加转堆计划')
            self.click("id","add")
            textInput=text(self.driver)
            self.logger.info('check1：验证计划号可否编辑')
            check.is_false(textInput.text_isenable("计划号"))
            if input["堆场"] != None:
                textInput.select_by_index("堆场",input['堆场'])
            if input["目标位置箱区"] != None:
                textInput.select_by_placeholder("请选择箱区", input['目标位置箱区'])
                textInput.select_by_placeholder("请选择倍位号", input['目标位置倍位号'])
            if input["备注"] != None:
                textInput.textarea_by_label("备注", input['备注'])
            self.click("xpath","//button//span[contains(text(),'选择箱')]")
            self.addWorkOrder(input, boxNumber)
            createTime=DataTime.GetTime()
            self.logger.info('check2：验证添加主计划弹出提示信息')
            self.check_alert(input["addplanalert"])
        except:
            self.click("x","//button//span[text()='取消']")
        tableCheck=Table(self.driver)
        self.logger.info('check3：验证添加后列表的值正确')
        config.planNumber=tableCheck.get_value("计划号")
        check.equal(tableCheck.get_value("目标位置"),input['目标位置箱区']+"-"+input['目标位置倍位号'])
        check.equal(tableCheck.get_value("备注"),input['备注'])
        check.equal(tableCheck.get_value("计划状态"), "执行")
        check.less(DataTime.get_dif_time(tableCheck.get_value("创建时间"), createTime), 300)
        check.less(DataTime.get_dif_time(tableCheck.get_value("录入时间"),createTime),300)
        check.equal(tableCheck.get_value("录入人"), config.createName)
        check.equal(tableCheck.get_value("创建人"), config.createName)



    def addWorkOrder(self, input,boxNumber):
        try:
            self.logger.info('步骤1：添加作业指令')
            #self.click("xpath","(//div[@id='add'])[2]")
            textInput = text(self.driver)
            textInput.input_by_placeholder("请输入箱号", boxNumber)
            self.click("xpath", "(//button//span[text()='检索'])[2]")
            tableCheck = ELtable(self.driver)
            self.logger.info('check3：验证添加作业指令窗口中列表的值正确')
            check.is_in(tableCheck.get_value("堆场"), input['堆场'])
            check.equal(tableCheck.get_value("箱号"), boxNumber)
            check.equal(tableCheck.get_value("尺寸"), input['尺寸'])
            check.is_in(tableCheck.get_value("箱型"), input['箱型'])
            check.equal(tableCheck.get_value("箱高"), input['箱高'])
            check.equal(tableCheck.get_value("箱状态"), "已落箱")
            tableCheck.click_row(1)
            self.click("xpath","//button//span[contains(text(),'确认')]")
        except:
            self.cancel()