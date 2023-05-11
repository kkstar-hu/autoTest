import time
import pytest_check as check
from Base.basepage import BasePage
from Commons.DateTime import DataTime
from GTOSXM.Controls.text import Gtos_text
from GTOSXM.Config import config
from GTOSXM.Controls.Gtos_table import Gtos_table


class Structure_Monitoring(BasePage):
    """
    有结构船舶监控
    """

    def Retrieve(self, input, boxnumber):
        """
        输入内容，检索
        """
        self.logger.info('有结构船舶监控-查询：' + input["船舶代码"])
        textinput = Gtos_text(self.driver)
        textinput.search_select_by_label('船舶查询', input["船舶中文名称"])
        self.click('xpath', "//span[text()='检索']")
        textinput.left_click('x', f"//div[text()='{boxnumber}']")
        self.click('xpath', "//span[text()='确 认']")
        self.check_alert('检查通过')
        self.close_alert('检查通过')

    def mouse_job(self):
        """
        框选操作
        """
        self.logger.info('有结构船舶监控-框选')
        self.clickandhold("x", "//div[@data-hno='01']")
        self.move_mouse_to_element("x", "//div[@data-hno='05']")
        self.move_release()
        time.sleep(3)

    def new_windows_choicebox(self, boxnumber):
        """
        新窗口操作
        """
        self.logger.info('有结构船舶监控-选箱')
        self.click('x', "//span[text()='箱查找']")
        self.input_no_clear('x', "//textarea[@placeholder='请输入箱号']", boxnumber)
        self.left_click('x', "//button//span[text()='查找']")
        self.click('x', "//button//span[text()='选择箱']")
        self.click('x', "//span[text()='箱号查找']//..//..//button[@aria-label='Collapse']")
        self.drag_mouse_to_element('x', "//span[text()='箱号查找']", 'x', "//span[text()='关闭所有舱']")

    def new_windows_job(self):
        """
        新窗口作业顺序
        """
        self.logger.info('有结构船舶监控-安排作业顺序')
        self.click('x', "//span[text()='作业顺序']")
        time.sleep(1)
        self.click('x', "//span[text()='按层从左到右']")
        self.click('x', "//span[text()='保 存']")
        time.sleep(1)
        self.check_alert('排序成功')
        self.close_alert('排序成功')

    def new_windows_sendbox(self):
        """
        新窗口发箱
        """
        self.logger.info('有结构船舶监控-发箱')
        self.click('x', "//span[text()='箱号查找']//..//..//..//button[@aria-label='Collapse']")
        self.click('x', "//button//span[text()='选择箱']")
        self.click('x', "//span[text()='箱号查找']//..//..//button[@aria-label='Collapse']")
        self.click('x', "//span[text()='发箱']")
        time.sleep(1)

    def selective_bridge(self, boxnumber):
        """
        选择吊桥
        """
        if boxnumber == config.outBoxNumber or boxnumber == config.boxNumber:
            self.left_click('x', "//input[@readonly='readonly']")
            time.sleep(1)
            self.left_click('x', "//span[text()='AUTO']")
            self.click('x', "//span[text()='发 箱']")
            self.check_alert('发箱成功')
            self.close_alert('发箱成功')
            self.close()
        if boxnumber == config.boxNumberTwo or boxnumber == config.boxNumberThree:
            self.click('x', "//span[text()='确 定']")
            self.check_alert('操作成功')
            self.close_alert('操作成功')
            self.close()

    def direct_job(self, name, job):
        """
        允许直提
        """
        self.logger.info('有结构船舶监控-特殊作业')
        self.click('x', "//span[text()='箱号查找']//..//..//..//button[@aria-label='Collapse']")
        self.click('x', "//button//span[text()='选择箱']")
        self.click('x', "//span[text()='箱号查找']//..//..//button[@aria-label='Collapse']")
        self.click('x', "//span[text()='特殊作业']")
        time.sleep(1)
        self.click('x', f"//span[text()='{name}']")
        time.sleep(1)
        self.click('x', f"//span[text()='{job}']")
        time.sleep(1)

    def LadeShip_Send_Box(self, boxnumber):
        """
        发箱
        """
        self.logger.info('有结构船舶监控-装船发箱' + boxnumber)
        table = Gtos_table(self.driver)
        table.left_click('x', "//span[text()='发箱']")
        time.sleep(1)
        table.left_click('id', "send-hatch")
        time.sleep(1)
        text = Gtos_text(self.driver)
        text.select_by_label('舱号', '01')
        text.select_by_label('CWP', 'A101')
        self.click('x', "//span[text()='查找']")
        table.check('箱号', boxnumber)
        tablecheck = Gtos_table(self.driver)
        if boxnumber == config.boxNumber:
            check.equal(tablecheck.get_value_by_rowid(config.boxNumber, '作业状态'), '可作业')
            self.click('x', "//button//span[text()='发箱']")
            self.check_alert('发箱成功')
            self.close_alert('发箱成功')
            check.equal(tablecheck.get_value_by_rowid(config.boxNumber, '作业状态'), '发箱')
        if boxnumber == config.outBoxNumber:
            check.equal(tablecheck.get_value_by_rowid(config.outBoxNumber, '作业状态'), '提交中控')
            self.click('x', "//button//span[text()='发箱']")
            self.check_alert('发箱成功')
            self.close_alert('发箱成功')
            check.equal(tablecheck.get_value_by_rowid(config.outBoxNumber, '作业状态'), '发箱')

    def ship_operation(self):
        """
        靠泊，桥吊操作
        """
        self.logger.info('有结构船舶监控-靠泊操作')
        self.click('x', "//span[text()='视图']")
        time.sleep(1)
        self.click('x', "//span[text()='靠离泊']")
        time.sleep(1)
        self.click('x', "//span[text()='靠泊确认']")
        textInput = Gtos_text(self.driver)
        stopTime = DataTime.Get_Current_Date() + " 00:00:00"
        textInput.input_by_label('靠泊时间', stopTime)
        textInput.input_by_label("靠泊吃水", '1')
        self.click('x', "//span[text()='提交']")
        self.check_alert_and_close('提交成功')
        self.logger.info('有结构船舶监控-分配桥吊')
        time.sleep(1)
        self.click('x', "(//span[text()='作业路'])[2]")
        time.sleep(1)
        self.click('x', "//span[text()='加载作业路']")
        self.left_click('x', "(//div[@class='grid'])[1]//span[text()='导入']")
        self.check_alert_and_close('保存成功')
        self.click('x', "//i[@class='el-dialog__close el-icon el-icon-close']")
        self.logger.info('有结构船舶监控-桥吊开工')
        self.click('x', "(//span[text()='作业路'])[2]")
        time.sleep(1)
        self.click('x', "//span[text()='作业路管理']")
        tablecheck1 = Gtos_table(self.driver)
        check.equal(tablecheck1.Big_get_value('状态'), '计划')
        self.click('x', "//span[@class='el-checkbox__inner']")
        time.sleep(1)
        self.input_by_index('x', "//input[@type='code']", 2, 0)
        self.input_by_index('x', "//input[@type='code']", 2, 1)
        self.click('x', "//span[text()='开工']")
        check.equal(tablecheck1.Big_get_value('状态'), '作业/开工')
        self.check_alert_and_close('开工成功。')
        self.click('x', "//i[@class='el-dialog__close el-icon el-icon-close']")

    def close_bridge(self):
        """
        离泊，桥吊完工操作
        """
        self.logger.info('有结构船舶监控-桥吊完工')
        self.click('x', "(//span[text()='作业路'])[2]")
        time.sleep(0.5)
        self.click('x', "//span[text()='作业路管理']")
        tablecheck1 = Gtos_table(self.driver)
        check.equal(tablecheck1.Big_get_value('状态'), '作业/开工')
        self.click('x', "//span[@class='el-checkbox__inner']")
        self.click('x', "//span[text()='完工']")
        check.equal(tablecheck1.Big_get_value('状态'), '完工')
        self.check_alert_and_close('AUTO 完工成功')
        self.click('x', "//i[@class='el-dialog__close el-icon el-icon-close']")
        time.sleep(1)

    def leave_port(self):
        """
        离泊
        """
        self.logger.info('有结构船舶监控--离泊操作')
        self.click('x', "//span[text()='视图']")
        time.sleep(0.5)
        self.click('x', "//span[text()='靠离泊']")
        time.sleep(0.5)
        self.click('x', "//span[text()='离泊确认']")
        time.sleep(0.5)
        self.click('x', "//span[@class='el-checkbox__inner']")
        leaveTime = DataTime.Get_Current_Date() + " 00:00:00"
        textInput = Gtos_text(self.driver)
        textInput.input_no_clear('x', "//input[@placeholder='离泊吃水']", '1')
        textInput.input_by_label('离泊时间', leaveTime)
        self.click('x', "//span[text()='提交']")
        self.check_alert('提交成功')
        self.close_alert('提交成功')
