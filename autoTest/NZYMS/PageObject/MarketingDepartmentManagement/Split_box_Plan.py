from selenium.webdriver.common.by import By
from Base.basepage import BasePage
from Commons.Controls.el_table import ELtable
from Commons.Controls.table import Table
from Commons.Controls.text import text
from Commons.DateTime import DataTime
from NZYMS.config import config
import pytest_check as check

class Split_Box_Plan(BasePage):
    """
    拆箱计划
    """
    def addPlan(self,input):
        """
        新增计划
        """
        try:
            self.logger.info('拆箱计划：添加主计划')
            self.click('xpath',"//div[@id='add']")
            self.waitloading()
            textInput = text(self.driver)
            self.logger.info('拆箱计划：输入内容')
            if input['堆场'] is not None:
                textInput.select_by_index('堆场',input['堆场'],1)
            if input['结算主体'] is not None:
                textInput.select_by_index('结算主体', input['结算主体'], 1)
            textInput.special_input("客户", "SHA", "SHAPGJHWYS/上海永旭集装箱运输")
            textInput.get_element('xpath',"//textarea[@placeholder='请输入备注']").send_keys(input['备注'])
            self.save_and_close()
            createTime = DataTime.GetTime()
            self.logger.info('check1：验证添加主计划弹出提示信息')
            self.check_alert_and_close(input["addplanalert"])
        except:
            self.click("x", "//button//span[text()='取消 ']")
        tableCheck = Table(self.driver,2)
        self.logger.info('check3：验证添加后列表的值正确')
        config.splitboxNumber = tableCheck.get_value("计划号")
        self.logger.info("拆箱计划号:" + config.splitboxNumber)
        check.equal(tableCheck.get_value("客户"), "上海永旭集装箱运输")
        tableCheck1 = Table(self.driver)
        check.is_in(tableCheck1.get_value("堆场"), input['堆场'])
        check.equal(tableCheck1.get_value("备注"), input['备注'])
        check.less(DataTime.get_dif_time(createTime,tableCheck1.get_value("创建时间")), 300)
        check.equal(tableCheck1.get_value("创建人"), config.createName)

    def addBoxPlan(self,input):
        """
        新增箱信息
        """
        self.logger.info('拆箱计划：添加计划箱')
        self.click_by_index('xpath',"//div[@id='add']",1)
        self.waitloading()
        textInput = text(self.driver)
        textInput.click('xpath', '//div[@class="vxe-modal--box"]//label[contains(text(),"堆场")]//following-sibling::div//input')
        textInput.get_elements('xpath', f"//div[@class='el-scrollbar']//span[text()='{input['堆场']}']")[1].click()
        textInput.input_by_placeholder("请输入箱号", config.boxNumberOutPlan)
        self.click_by_index("xpath", "(//button//span[text()='检索'])",1)
        tableCheck = ELtable(self.driver)
        row = self.rows()
        self.logger.info('check1：验证添加作业指令窗口中列表的值正确')
        check.is_in(tableCheck.get_value_by_trElement("箱号", config.boxNumberOutPlan, "堆场"), input['堆场'])
        check.equal(tableCheck.get_value_by_trElement("箱号", config.boxNumberOutPlan, "尺寸"), input['尺寸'])
        check.is_in(tableCheck.get_value_by_trElement("箱号", config.boxNumberOutPlan, "箱型"), input['箱型'])
        check.equal(tableCheck.get_value_by_trElement("箱号", config.boxNumberOutPlan, "箱高"), input['箱高'])
        check.equal(tableCheck.get_value_by_trElement("箱号", config.boxNumberOutPlan, "进场类型"),input['进场作业类型'])
        tableCheck.select_row("箱号",config.boxNumberOutPlan)
        self.click("xpath","//button//span[contains(text(),'确认')]")

    def addCar(self,input):
        """
        新增车辆信息
        """
        try:
            self.logger.info('拆箱计划：添加车辆')
            self.click_by_index('xpath',"//div[@id='add']",1)
            self.waitloading()
            textInput = text(self.driver)
            if input['车牌'] is not None:
                textInput.select_by_label("车牌", input['车牌'])
            if input['车号'] is not None:
                self.get_element('xpath', "//input[@placeholder='请输入车号']").send_keys(input['车号'])
            self.element_wait_disappear(By.XPATH, "//div[@role='alert']//p")
            self.save_and_close()
        except:
            self.cancel()
        createTime = DataTime.GetTime()
        self.logger.info('check1：验证新增车辆信息弹出提示信息')
        self.check_alert(input["addcaralert"])
        tableCheck = Table(self.driver,6)
        self.logger.info('check2：验证添加后列表的值正确')
        check.equal(tableCheck.get_value("车牌号"), input['车牌']+input['车号'])
        check.less(DataTime.get_dif_time(createTime,tableCheck.get_value("创建时间")), 300)
        check.equal(tableCheck.get_value("创建人"), config.createName)

    def switch_box_information(self):
        """
        切换箱信息
        """
        self.click('xpath',"//div[contains(text(),'箱信息')]")

    def switch_goods_information(self):
        """
        切换车辆信息
        """
        self.click('xpath',"//div[contains(text(),'车辆信息')]")

    def more_information(self,row):
        """
        ...鼠标点击
        """
        self.logger.info('拆箱计划：展开...')
        table= Table(self.driver,3)
        table.moreButton(row)
        self.element_wait('id','setup')

    def perform_tasks(self):
        """
        执行按钮（后期可能需要增加判断选择了是 取消 执行 关闭 等操作，给出 对应提示）
        """
        self.more_information(1)
        self.logger.info('拆箱计划：执行')
        self.click('xpath', "//li[@class='el-menu-item']//span[text()='执行']")
        self.element_wait_disappear(By.XPATH, "//div[@role='alert']//p")
        self.click("xpath", "//div[@class='el-message-box__btns']//span[contains(text(),'确定')]")
        self.check_alert("执行成功")
        tableCheck = Table(self.driver,2)
        self.logger.info('check3：验证执行按钮后计划状态变执行状态')
        check.equal(tableCheck.get_value("计划状态"), "执行")
