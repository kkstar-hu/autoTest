from Base.basepage import BasePage
from Commons.Controls.text import text
from Commons.Controls.table import Table
from Commons.DateTime import DataTime
from NZYMS.config import config
import pytest_check as check


class LockBox(BasePage):

    def search(self,input):
        textInput = text(self.driver)
        textInput.input_by_label("箱号",config.boxNumber)
        textInput.select_by_label("堆场", input["堆场"])
        textInput.select_by_label("结算主体", input["结算主体"])
        self.click("xpath","//button//span[text()='检索']")

    def checkboxInformation(self,input):
        tablecheckfixed = Table(self.driver, 2)
        check.is_in(tablecheckfixed.get_value("结算主体"), input["结算主体"])
        check.equal(tablecheckfixed.get_value("箱号"), config.boxNumber)
        tablecheck = Table(self.driver, 1)
        check.equal(tablecheck.get_value("持箱人"), input["持箱人"])
        check.equal(tablecheck.get_value("尺寸"), input["尺寸"])
        check.equal(tablecheck.get_value("箱高"), input["箱高"])
        check.equal(tablecheck.get_value("箱型"), input["箱型"])



    def lockbox(self,input):
        try:
            table=Table(self.driver,2)
            table.lockButton(config.boxNumber)
            self.click_by_index("xpath",f"//form[@class='el-form']//label[contains(text(),'锁定原因')]//following-sibling::div//input",1)
            self.click("xpath", f"//div[@class='el-scrollbar']//span[text()='{input['锁定原因']}']")
            self.click("xpath", "//button//span[text()='确认']")
            self.check_alert(input["alert"])
            self.close_alert(input["alert"])
        except:
            self.cancel()
        if input["alert"] == "加锁成功":
            createTime = DataTime.GetTime()
            tableOperation = Table(self.driver, 3)
            check.equal(tableOperation.get_value("是否锁定"), "是")
            tablecheck = Table(self.driver, 4)
            tablecheck.down_arrow_sort("锁箱时间")
            check.equal(tablecheck.get_value("是否高级锁"), "否")
            check.equal(tablecheck.get_value("锁箱人"), config.createName)
            check.less(DataTime.get_dif_time(createTime,tablecheck.get_value("锁箱时间")), 300)
            check.equal(tablecheck.get_value("锁箱备注"), input["锁定原因"])


    def superlockbox(self, input):
        try:
            table = Table(self.driver, 2)
            table.superlockButton(config.boxNumber)
            self.click_by_index("xpath",f"//form[@class='el-form']//label[contains(text(),'锁定原因')]//following-sibling::div//input",1)
            self.click("xpath", f"//div[@class='el-scrollbar']//span[text()='{input['锁定原因']}']")
            self.click("xpath", "//button//span[text()='确认']")
        except:
            self.cancel()
        self.check_alert(input["alert"])
        self.close_alert(input["alert"])
        if input["alert"] == "加锁成功":
            createTime = DataTime.GetTime()
            tableOperation = Table(self.driver, 3)
            check.equal(tableOperation.get_value("是否锁定"), "是")
            tablecheck = Table(self.driver, 4)
            check.equal(tablecheck.get_value("是否高级锁"), "是")
            check.equal(tablecheck.get_value("锁箱人"), config.createName)
            check.less(DataTime.get_dif_time(tablecheck.get_value("锁箱时间"), createTime), 300)
            check.equal(tablecheck.get_value("锁箱备注"), input["锁定原因"])


    def unlockbox(self, input):
        tablecheck = Table(self.driver, 4)
        self.click("xpath", f"(//table[@class='vxe-table--body'])[4]/tbody//tr[1]//div[contains(text(),'解锁')]")
        self.click("xpath", "//button//span[contains(text(),'确定')]")
        self.check_alert(input["unlockalert"])
        self.close_alert(input["unlockalert"])
        createTime = DataTime.GetTime()
        if input["unlockalert"] == "解锁成功":
            check.equal(tablecheck.get_last_row_value("解锁人"), config.createName)
            check.less(createTime,DataTime.get_dif_time(tablecheck.get_value("解锁时间")), 300)




