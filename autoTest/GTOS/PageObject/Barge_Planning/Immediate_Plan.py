import time
import pytest_check as check
from Base.basepage import BasePage
from GTOS.Controls.text import Gtos_text
from GTOS.Config import config
from GTOS.Controls.Gtos_table import Gtos_table


class Immediate_plan(BasePage):
    """
    驳船策划--近期计划
    """
    def switch_Barge(self):
        """
        切换驳船计划
        """
        self.logger.info('步骤1：切换驳船计划')
        self.click('xpath',"//div[contains(text(),'驳船船期计划')]")

    def Add_Plan(self,input):
        """
        新增船期
        """
        # self.logger.info('步骤2：新增船期')
        # self.click('xpath',"//span[contains(text(),'新增')]")
        # self.logger.info('步骤3：输入数据')
        textInput = Gtos_text(self.driver)
        # textInput.select_by_label("船舶代码", input["船舶代码"])
        # textInput.click_by_index('x',"(//input[@placeholder='选择日期时间'])",0)
        # self.click('xpath', "//span[contains(text(),'确定')]")
        # textInput.click_by_index('x',"(//input[@placeholder='选择日期时间'])",1)
        # self.click('xpath', "(//span[contains(text(),'确定')])[2]")
        # textInput.input_no_clear('xpath',
        #                           "(//td[@class='el-table_2_column_10_column_11   el-table__cell']/div//input)[1]",
        #                           input['出口航次'])
        # textInput.click('x',"//td[@class='el-table_2_column_12_column_13   el-table__cell']/div//input")
        # textInput.click('x',"(//div[@class='el-scrollbar']//span[text()='正常航次'])[2]")
        # textInput.click('x',"//td[@class='el-table_2_column_14_column_15   el-table__cell']/div//input")
        # textInput.click('x',"(//div[@class='el-scrollbar']//span[text()='内外贸'])[2]")
        # textInput.click('x',"//td[@class='el-table_2_column_16_column_17   el-table__cell']/div//input")
        # textInput.click('x',"(//div[@class='el-scrollbar']//span[text()='阳逻二期'])[2]")
        # textInput.click('x',"(//td[@class='el-table_2_column_18_column_19   el-table__cell']/div//input)[1]")
        # textInput.click('x',"(//div[@class='el-scrollbar']//span[text()='出口'])[4]")
        # textInput.click('x',"//td[@class='el-table_2_column_20_column_21   el-table__cell']/div//input")
        # textInput.click('x',"(//div[@class='el-scrollbar']//span[text()='汉申线（外港快航）'])[2]")
        # self.logger.info('步骤4：新增进口航次')
        # self.click('xpath', "(//span[contains(text(),'新增')])[4]")
        # textInput.input_no_clear('xpath',
        #                           "(//td[@class='el-table_2_column_10_column_11   el-table__cell']/div//input)[2]",
        #                           input['进口航次'])
        # textInput.click('x',"(//td[@class='el-table_2_column_18_column_19   el-table__cell']/div//input)[2]")
        # textInput.click('x',"(//div[@class='el-scrollbar']//span[text()='进口'])[8]")
        # textInput.input_by_label('起始尺码','100')
        # textInput.select_by_label('船尾揽桩','2')
        # # textInput.select_by_label('船头揽桩','1')
        # self.click('x',"//div[@placeholder='请选择船头揽桩']")
        # self.click('x',"(//span[text()='4'])[2]")
        # textInput.click('x',"//span[contains(text(),'保 存')]")
        textInput.input_noclear_placeholder_click('请输入关键词','DDZ/(DDZ)(DDZ驳船)/DDZE/I')
        textInput.click('x',"//span[text()='检索']")
        tablecheck = Gtos_table(self.driver,2)
        check.equal(tablecheck.get_value('船期状态'),'预报')
        self.click('x',"//span[text()='确报船期']")
        self.click('x',"//span[text()='保 存']")
        check.equal(tablecheck.get_value('船期状态'),'确报')



    def Immediate_plan_process(self,input):
        """
        近期计划流程
        """
        self.switch_Barge()
        self.Add_Plan(input)
        time.sleep(3)