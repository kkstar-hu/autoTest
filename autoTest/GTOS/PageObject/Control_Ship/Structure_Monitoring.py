import time
import pytest_check as check
from selenium.webdriver import ActionChains
from Base.basepage import BasePage
from Commons.DateTime import DataTime
from GTOS.Controls.text import Gtos_text
from GTOS.Config import config
from GTOS.Controls.Gtos_table import Gtos_table

class Structure_Monitoring(BasePage):
    """
    有结构船舶监控
    """
    def Retrieve(self,input,boxnumber):
        """
        输入内容，检索
        """
        self.logger.info('有结构船舶监控-查询：'+ input["船舶代码"])
        textinput = Gtos_text(self.driver)
        textinput.search_select_by_label('船舶查询',input["船舶代码"])
        self.click('xpath',"//span[text()='检索']")
        textinput.left_click('x',f"//div[text()='{boxnumber}']")
        self.click('xpath',"//span[text()='确 认']")
        self.check_alert('检查通过')
        self.close_alert('检查通过')


    def mouse_job(self):
        """
        框选操作
        """
        self.clickandhold("x",
                          "//div[@class='nzctos-lateral__body__deck nzctos-lateral__body__right']//div[@data-hno='05']")
        self.move_mouse_to_element("x",
                                   "//div[@class='nzctos-lateral__body__deck nzctos-lateral__body__right']//div[@data-hno='01']")
        self.move_release()
        time.sleep(1)

    def new_windows_job(self):
        """
        新窗口操作
        """
        pass



    def LadeShip_Send_Box(self,boxnumber):
        """
        发箱
        """
        self.logger.info('有结构船舶监控-装船发箱'+boxnumber)
        table = Gtos_table(self.driver)
        table.left_click('x',"//span[text()='发箱']")
        time.sleep(1)
        table.left_click('id',"send-hatch")
        time.sleep(1)
        text = Gtos_text(self.driver)
        text.select_by_label('舱号','01')
        text.select_by_label('CWP','A101')
        self.click('x',"//span[text()='查找']")
        table.check('箱号',boxnumber)
        tablecheck = Gtos_table(self.driver)
        if  boxnumber == config.boxNumber:
            check.equal(tablecheck.get_value_by_rowid(config.boxNumber, '作业状态'), '可作业')
            self.click('x',"//button//span[text()='发箱']")
            self.check_alert('发箱成功')
            self.close_alert('发箱成功')
            check.equal(tablecheck.get_value_by_rowid(config.boxNumber, '作业状态'), '发箱')
        if  boxnumber == config.outBoxNumber:
            check.equal(tablecheck.get_value_by_rowid(config.outBoxNumber, '作业状态'), '提交中控')
            self.click('x',"//button//span[text()='发箱']")
            self.check_alert('发箱成功')
            self.close_alert('发箱成功')
            check.equal(tablecheck.get_value_by_rowid(config.outBoxNumber, '作业状态'), '发箱')

    def ship_operation(self):
        """
        靠泊，桥吊操作
        """
        self.logger.info('有结构船舶监控-靠泊操作')
        self.click('x',"//span[text()='视图']")
        time.sleep(1)
        self.click('x',"//span[text()='靠离泊']")
        time.sleep(1)
        self.click('x',"//span[text()='靠泊确认']")
        self.click('x',"//input[@placeholder='靠泊时间']")
        self.click('x',"//span[contains(text(),'此刻')]")
        textInput = Gtos_text(self.driver)
        textInput.input_by_label("靠泊吃水",'1')
        self.click('x',"//span[text()='提交']")
        if self.get_text('x',"//div[@role='alert']//p") == '靠泊时间不能大于当前时间.':
            self.close_alert('靠泊时间不能大于当前时间.')
            time.sleep(2)
            self.click('x', "//span[text()='提交']")
        self.check_alert('提交成功')
        self.close_alert('提交成功')
        self.logger.info('有结构船舶监控-分配桥吊')
        self.click('x',"//span[text()='作业路']")
        time.sleep(1)
        self.click('x', "//span[text()='加载作业路']")
        self.left_click('x',"(//div[@class='grid'])[1]//span[text()='导入']")
        self.check_alert('保存成功')
        self.close_alert('保存成功')
        self.click('x',"//i[@class='el-dialog__close el-icon el-icon-close']")
        self.logger.info('有结构船舶监控-桥吊开工')
        self.click('x',"//span[text()='作业路']")
        time.sleep(1)
        self.click('x', "//span[text()='作业路管理']")
        tablecheck1 = Gtos_table(self.driver)
        check.equal(tablecheck1.Big_get_value('状态'),'计划')
        self.click('x',"//span[@class='el-checkbox__inner']")
        time.sleep(1)
        self.input_by_index('x',"//input[@type='code']",2,0)
        self.input_by_index('x',"//input[@type='code']",2,1)
        self.click('x',"//span[text()='开工']")
        check.equal(tablecheck1.Big_get_value('状态'),'作业/开工')
        self.check_alert('开工成功。')
        self.close_alert('开工成功。')
        self.click('x', "//i[@class='el-dialog__close el-icon el-icon-close']")

