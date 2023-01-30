import time
import pytest_check as check
from Base.basepage import BasePage
from Commons.Controls.el_table import ELtable
from Commons.DateTime import DataTime
from GTOS.Controls.text import Gtos_text
from GTOS.Config import config
from GTOS.Controls.Gtos_table import Gtos_table


class Immediate_plan(BasePage):
    """
    驳船策划--近期计划
    """
    arriveDay = DataTime.Get_Current_Date()
    arriveTime = arriveDay + " 00:00:00"
    leaveDay = DataTime.Get_Date_X_Number_Of_Days(20)
    leaveTime = leaveDay + " 00:00:00"
    def switch_Barge(self):
        """
        切换驳船计划
        """
        self.click('xpath',"//div[contains(text(),'驳船船期计划')]")

    def Add_Plan(self, input):
        self.click('xpath', "//span[contains(text(),'新增')]")
        textInput = Gtos_text(self.driver)
        textInput.select_by_label("船舶代码", input["船舶代码"])
        textInput.input_by_label("抵港时间",self.arriveTime)
        self.click('xpath', "//span[contains(text(),'确定')]")
        textInput.input_by_label("离港时间",self.leaveTime)
        self.click('xpath', "(//span[contains(text(),'确定')])[2]")
        eltable=ELtable(self.driver,2)
        eltable.input_text("航次",config.outportNumber)
        eltable.input_select("航次类型", input["航次类型"])
        eltable.input_select("贸易类型", input["贸易类型"])
        eltable.input_select("归属码头", input["归属码头"])
        eltable.input_select("海关进出口", input["海关进出口1"])
        eltable.input_select("营运人航线", input["营运人航线"])
        self.click('xpath', "(//span[contains(text(),'新增')])[4]")
        eltable.input_text("航次",config.importNumber,2)
        eltable.input_select("航次类型", input["航次类型"],2)
        eltable.input_select("贸易类型", input["贸易类型"],2)
        eltable.input_select("归属码头", input["归属码头"],2)
        eltable.input_select("海关进出口", input["海关进出口2"],2)
        eltable.input_select("营运人航线", input["营运人航线"],2)
        textInput.input_by_label('起始尺码', input["起始尺码"])
        textInput.select_by_label('船尾揽桩',input["船尾揽桩"])
        textInput.select_by_label_time('船头揽桩',input["船头揽桩"])
        textInput.click('x',"//span[contains(text(),'保 存')]")
        check.equal(self.get_text("xpath", "//div[@role='alert']//h2"), "添加成功")

    def checkPlan(self):
        self.click('x', "//span[text()='检索']")
        tablecheck = Gtos_table(self.driver, 2)
        rowid=tablecheck.select_row("进口航次",config.importNumber)
        self.logger.info('进口航次号为：'+tablecheck.get_value_by_rowid(rowid,'进口航次'))
        self.logger.info('出口航次号为：'+tablecheck.get_value_by_rowid(rowid,'出口航次'))
        check.equal(tablecheck.get_value_by_rowid(rowid,'船期状态'), '预报')
        check.equal(tablecheck.get_value_by_rowid(rowid, '靠泊状态'), '未靠')
    def Sure_ShipPlan(self):
        textInput = Gtos_text(self.driver)
        actualarriveDay = DataTime.Get_Current_Date()
        actuallarriveTime = actualarriveDay + " 00:00:00"
        self.click('x', "//span[text()='确报船期']")
        textInput.input_by_label("实际抵港时间", actuallarriveTime)
        self.click('xpath', "//span[contains(text(),'确定')]")
        self.click('x', "//span[text()='保 存']")
        check.equal(self.get_text("xpath", "//div[@role='alert']//h2"), "保存成功")
        tablecheck = Gtos_table(self.driver, 2)
        check.equal(tablecheck.get_value('船期状态'), '确报')
        check.equal(tablecheck.get_value('确报时间'), actuallarriveTime)

    #点击确认进箱
    def SureInBox(self):
        self.click('id', "confirmintocntr")
        self.click('x', "(//span[@class='el-switch__core'])[2]")
        self.click('x', "//span[text()='保 存']")
        check.equal(self.get_text("xpath", "//div[@role='alert']//h2"), "保存成功")

    #验证靠泊信息
    def check_alongside_info(self,input):
        tablecheck = Gtos_table(self.driver, 2)
        rowid = tablecheck.select_row("进口航次", config.importNumber)
        check.equal(self.get_text_value("计划靠泊时间"), self.arriveTime)
        check.equal(self.get_text_value("计划离泊时间"), self.leaveTime)
        check.equal(self.get_text_value("计划靠泊泊位"), "01")
        check.equal(self.get_text_value("计划靠泊吃水"), "0")
        check.equal(self.get_text_value("计划起始尺码"), input["起始尺码"])
        check.equal(self.get_text_value("计划终止尺码"), "270")
        createTime = DataTime.GetTime()
        #check.less(DataTime.get_dif_time(self.get_text_value("实际靠泊时间"), createTime), 900)
        #check.less(DataTime.get_dif_time(self.get_text_value("实际离泊时间"), createTime), 300)
        #print(createTime)
        #print(self.get_text_value("实际离泊时间"))
        check.equal(self.get_text_value("实际靠泊吃水"), "0")
        check.equal(self.get_text_value("实际起始尺码"), input["起始尺码"])
        check.equal(self.get_text_value("实际终止尺码"), "270")
        check.equal(self.get_text_value("船头揽桩"), input["船头揽桩"])
        check.equal(self.get_text_value("船尾揽桩"), input["船尾揽桩"])

    #靠泊信息获取值方法
    def get_text_value(self,label):
        return self.get_text("xpath",f"//div[contains(text(),'{label}')]//following-sibling::div")


