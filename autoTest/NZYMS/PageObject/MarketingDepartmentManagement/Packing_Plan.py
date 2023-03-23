import time

from selenium.webdriver.common.by import By

from Base.basepage import BasePage
from Commons.Controls.el_table import ELtable
from Commons.Controls.table import Table
from Commons.Controls.text import text
from Commons.DateTime import DataTime
from NZYMS.config import config
import pytest_check as check
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait



class Packing_Plan(BasePage):
    """
    装箱计划
    """

    def addPlan(self,input):
        """
        新增计划
        """
        try:
            self.logger.info('装箱计划：添加主计划')
            self.click('xpath',"//div[@id='add']")
            textInput = text(self.driver)
            self.logger.info('装箱计划：输入内容')
            if input['结算主体'] is not None:
                textInput.select_by_index('结算主体', input['结算主体'], 1)
            if input['堆场'] is not None:
                textInput.select_by_index('堆场', input['堆场'], 1)
            textInput.special_input("客户", "SHA", "SHAPGJHWYS/上海永旭集装箱运输")
            textInput.get_element('xpath',"//textarea[@placeholder='请输入']").send_keys(input['备注'])
            self.save_and_close()
            createTime = DataTime.GetTime()
            self.logger.info('check1：验证添加主计划弹出提示信息')
            self.check_alert(input["addplanalert"])
        except:
            self.click("x","//button//span[text()='取消 ']")
        tableCheck = Table(self.driver,2)
        self.logger.info('check3：验证添加后列表的值正确')
        config.packingboxNumber = tableCheck.get_value("计划号")
        self.logger.info("装箱计划号:" + config.packingboxNumber)
        check.equal(tableCheck.get_value("客户"), "上海永旭集装箱运输")
        tableCheck1 = Table(self.driver)
        check.is_in(tableCheck1.get_value("堆场"), input['堆场'])
        check.equal(tableCheck1.get_value("备注"), input['备注'])
        check.less(DataTime.get_dif_time(createTime,tableCheck1.get_value("创建时间")), 100)
        check.equal(tableCheck1.get_value("创建人"), config.createName)


    def addBoxPlan(self,input):
        """
        新增箱信息
        """
        try:
            self.logger.info('装箱计划：添加计划箱')
            self.click_by_index('xpath',"//div[@id='add']",1)
            self.waitloading()
            textInput = text(self.driver)
            textInput.select_by_index('堆场', input['堆场'], 1)
            textInput.input_by_placeholder("请输入箱号",config.boxNumberOutPlan)
            self.click_by_index("xpath", "(//button//span[text()='检索'])",1)
            tableCheck = ELtable(self.driver)
            self.logger.info('check3：验证添加作业指令窗口中列表的值正确')
            check.is_in(tableCheck.get_value_by_trElement("箱号", config.boxNumberOutPlan, "堆场"), input['堆场'])
            check.equal(tableCheck.get_value_by_trElement("箱号", config.boxNumberOutPlan, "尺寸"), input['尺寸'])
            check.is_in(tableCheck.get_value_by_trElement("箱号", config.boxNumberOutPlan, "箱型"), input['箱型'])
            check.equal(tableCheck.get_value_by_trElement("箱号", config.boxNumberOutPlan, "箱高"), input['箱高'])
            check.equal(tableCheck.get_value_by_trElement("箱号", config.boxNumberOutPlan, "进场类型"),input['进场作业类型'])
            tableCheck.select_row("箱号",config.boxNumberOutPlan)
            self.click("xpath","//button//span[contains(text(),'确认')]")
        except:
            self.click("x", "//button//span[text()='取消']")

    def switch_box_information(self):
        """
        切换箱信息
        """
        self.click('xpath',"//div[contains(text(),'箱信息')]")

    def switch_goods_information(self):
        """
        切换货物信息
        """
        self.click('xpath',"//div[contains(text(),'货物信息')]")

    def addGoods_stow(self,input):
        """
        新增货物信息,直装货
        """
        try:
            self.logger.info('装箱计划：添加货物信息')
            self.click_by_index('xpath',"//div[@id='add']",1)
            self.waitloading()
            textInput = text(self.driver)
            if input['车牌'] is not None:
                textInput.select_by_label("车牌", input['车牌'])
            if input['车号'] is not None:
                self.get_element('xpath', "//input[@placeholder='请输入车牌号']").send_keys(input['车号'])
            if input['仓库'] is not None:
                textInput.select_by_label('仓库', input['仓库'])
            textInput.input_by_label('提单号',input['提单号'])
            textInput.input_by_label('分提单',input['分提单'])
            textInput.input_by_label('货名',input['货名'])
            textInput.input_by_label('唛头',input['唛头'])
            textInput.input_by_label('包装',input['包装'])
            textInput.input_by_label('件数', input['件数'])
            textInput.input_by_label('体积', input['体积'])
            textInput.input_by_label('重量(kg)', input['重量(kg)'])
            self.save_and_close()
        except:
            self.cancel()
        createTime = DataTime.GetTime()
        self.check_alert(input["addgoodsalert"])
        tableCheck = Table(self.driver,4)
        self.logger.info('check3：验证添加后列表的值正确')
        check.equal(tableCheck.get_value("提单号"), input['提单号'])
        check.equal(tableCheck.get_value("分提单"), input['分提单'])
        check.equal(tableCheck.get_value("货名"), input['货名'])
        check.equal(tableCheck.get_value("唛头"), input['唛头'])
        check.equal(tableCheck.get_value("包装"), input['包装'])
        check.equal(tableCheck.get_value("计划件数"), input['件数'])
        check.equal(tableCheck.get_value("计划体积"), input['体积'])
        check.equal(tableCheck.get_value("计划重量(kg)"), input['重量(kg)'])
        check.equal(tableCheck.get_value("车牌号"), input['车牌']+input['车号'])
        check.less(DataTime.get_dif_time(createTime,tableCheck.get_value("创建时间")), 300)
        check.equal(tableCheck.get_value("创建人"), config.createName)

    def addGoods_warehouse(self, input):
        """
        新增货物信息，库内货
        """
        self.logger.info('装箱计划：添加货物信息')
        self.click('xpath',"//span[text()='入库明细追加']")
        self.waitloading()
        textInput = text(self.driver)
        textInput.select_by_index('堆场',input['堆场'],1)
        self.click_by_index('xpath',"//span[text()='检索']",1)
        table = Table(self.driver,6)
        table.check("计划号", config.bulkintoNumber)
        self.click('xpath',"//span[text()='确认']")


    def choice_addGoods(self,input):
        """
        选择如何新增货物信息
        """
        if input['新增货物方式'] == '新增':
            self.addGoods_stow(input)
        else:
            self.addGoods_warehouse(input)


    def more_information(self,row):
        """
        ...鼠标点击
        """
        self.logger.info('步骤1：展开...')
        table= Table(self.driver,3)
        table.moreButton(row)
        self.element_wait('id','setup')


    def perform_tasks(self):
        """
        执行按钮（后期可能需要增加判断选择了是 取消 执行 关闭 等操作，给出 对应提示）
        """
        self.more_information(1)
        self.logger.info('装箱计划：执行')
        self.click('id', 'setup')
        self.element_wait_disappear(By.XPATH, "//div[@role='alert']//p")
        self.click("xpath", "//div[@class='el-message-box__btns']//span[contains(text(),'确定')]")
        self.check_alert("执行成功")
        tableCheck = Table(self.driver,2)
        self.logger.info('check3：验证执行按钮后计划状态变执行状态')
        time.sleep(1)
        check.equal(tableCheck.get_value("计划状态"), "执行")

