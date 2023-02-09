from selenium.webdriver.common.by import By

from Base.basepage import BasePage
from Commons.Controls.el_table import ELtable
from Commons.Controls.table import Table
from Commons.Controls.text import text
from Commons.DateTime import DataTime
from NZYMS.Config import config
import pytest_check as check
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

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
            # self.logger.info('步骤2：刷新元素')
            # self.refresh()
            # self.click('xpath',"//div[@id='add']")
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
            self.check_alert(input["addplanalert"])
        except:
            self.click("x", "//button//span[text()='取消 ']")
        tableCheck = Table(self.driver,2)
        self.logger.info('check3：验证添加后列表的值正确')
        config.splitboxNumber = tableCheck.get_value("计划号")
        check.equal(tableCheck.get_value("客户"), "上海永旭集装箱运输")
        tableCheck1 = Table(self.driver)
        check.is_in(tableCheck1.get_value("堆场"), input['堆场'])
        check.equal(tableCheck1.get_value("备注"), input['备注'])
        check.less(DataTime.get_dif_time(tableCheck1.get_value("创建时间"), createTime), 300)
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
        check.is_in(tableCheck.get_value("堆场",row), input['堆场'])
        check.equal(tableCheck.get_value("箱号",row), config.boxNumberOutPlan)
        check.equal(tableCheck.get_value("尺寸",row), input['尺寸'])
        check.equal(tableCheck.get_value("箱型",row), input['箱型'])
        check.equal(tableCheck.get_value("箱高",row), input['箱高'])
        check.is_in(tableCheck.get_value("结算主体",row), input['结算主体'])
        check.is_in(tableCheck.get_value("进场类型",row), input['进场作业类型'])
        tableCheck.click_row(row)
        self.click("xpath","//button//span[contains(text(),'确认')]")

    def rows(self):
        """
        通过对列表循环，查找对应计划所在行数
        """
        pax = []
        att = []
        # 根据table xpath定位到表格
        table = self.get_elements('xpath','//*[@id="app"]/div[3]/section/div[1]/div[2]/div[1]/div/div[2]/div/div/div[2]/div[1]/div[2]/table')
        # 通过标签名获取表格的所有行
        table_tr_list = self.get_elements('xpath',"(//div[@class='el-table__body-wrapper is-scrolling-left'])//tr")
        #  按行查询表格的数据，取出的数据是一整行，按,分隔每一列的数据
        for tr in table_tr_list:
            att = (tr.text).split("\n")
            pax.append(att)
        for i in pax:
            if config.boxNumberOutPlan in i:
                return i[1]



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
            # WebDriverWait(self.driver, 5, 1).until_not(
            #     EC.presence_of_element_located((By.XPATH, "//div[@role='alert']//p")))
            self.save_and_close()
        except:
            self.cancel()
        createTime = DataTime.GetTime()
        self.logger.info('check1：验证新增车辆信息弹出提示信息')
        self.check_alert(input["addcaralert"])
        tableCheck = Table(self.driver,6)
        self.logger.info('check2：验证添加后列表的值正确')
        check.equal(tableCheck.get_value("车牌号"), input['车牌']+input['车号'])
        check.less(DataTime.get_dif_time(tableCheck.get_value("创建时间"), createTime), 300)
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
        # WebDriverWait(self.driver, 10, 1).until_not(
        #     EC.presence_of_element_located((By.XPATH, "//div[@role='alert']//p")))
        self.click("xpath", "//div[@class='el-message-box__btns']//span[contains(text(),'确定')]")
        self.check_alert("执行成功")
        tableCheck = Table(self.driver,2)
        self.logger.info('check3：验证执行按钮后计划状态变执行状态')
        check.equal(tableCheck.get_value("计划状态"), "执行")
