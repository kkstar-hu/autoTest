import time
import pytest_check as check
from Base.basepage import BasePage
from Commons.DateTime import DataTime
from GTOS.Controls.text import Gtos_text
from GTOS.Config import config
from GTOS.Controls.Gtos_table import Gtos_table


class Bridge_Crane_Distribution(BasePage):

    arriveDay = DataTime.Get_Current_Date()
    arriveTime = arriveDay + " 00:00:00"
    leaveDay = DataTime.Get_Date_X_Number_Of_Days(20)
    leaveTime = leaveDay + " 00:00:00"
    """
    驳船策划--桥吊资源分配
    """
    def search(self,input):
        """
        输入船名航次
        """
        self.logger.info('步骤1：选择船名航次')
        textInput = Gtos_text(self.driver)
        textInput.search_select_by_label('船名航次',config.importNumber)
        self.logger.info('步骤2：点击检索')
        self.click('x',"(//span[text()='检索'])[2]")
        tablecheck = Gtos_table(self.driver, 3)
        check.equal(tablecheck.get_value('船舶代码'), input['船舶代码'])
        check.equal(tablecheck.get_value('船舶中文名称'), input['船舶中文名称'])
        check.equal(tablecheck.get_value('船舶类型'), input['船舶类型'])
        check.equal(tablecheck.get_value('进口航次'), config.importNumber)
        check.equal(tablecheck.get_value('出口航次'), config.outportNumber)
        check.equal(tablecheck.get_value('计划靠泊时间'), self.arriveTime)
        check.equal(tablecheck.get_value('计划离泊时间'), self.leaveTime)
        check.equal(tablecheck.get_value('计划靠泊泊位'), '01')

    def arrangeBridge(self):
        """
        勾选内容，分配桥吊
        """
        self.logger.info('步骤3：勾选内容，分配桥吊')
        tablecheck = Gtos_table(self.driver,3)
        tablecheck.tick_off_box(1)
        tablecheck.click('x',"//span[text()='安排桥吊资源']")
        tablecheck.click('x',"//label//span[text()='B109']")
        tablecheck.click('x',"//span[text()='保 存']")
        check.equal(self.get_text("xpath","//div[@role='alert']//h2"),"保存成功")
        check.equal(tablecheck.get_value('桥吊号'), 'B109')
        check.equal(tablecheck.get_value('吊桥计划开始时间'), self.arriveTime)
        check.equal(tablecheck.get_value('吊桥计划结束时间'), self.leaveTime)


