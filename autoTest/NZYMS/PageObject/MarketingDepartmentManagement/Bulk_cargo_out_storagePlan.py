import time

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from Base.basepage import BasePage
from Commons.Controls.table import Table
from Commons.Controls.text import text
from Commons.DateTime import DataTime
from NZYMS.Config import config
import pytest_check as check

class Bulk_cargo_out_storagePlan(BasePage):
    """
    散货出库计划
    """
    def addPlan(self,input):
        """
        新增散货出库计划
        """
        try:
            self.waitloading()
            self.logger.info('散货出库计划：添加主计划')
            self.click('xpath',"//div[@id='add']")
            self.waitloading()
            textInput = text(self.driver)
            self.logger.info('散货出库计划：输入内容')
            if input['结算主体'] is not None:
                textInput.select_by_index('结算主体',input['结算主体'],1)
            if input['计划类型'] is not None:
                textInput.select_by_index('计划类型',input['计划类型'],1)
            if input['堆场'] is not None:
                textInput.select_by_index('堆场',input['堆场'],1)
            if input['仓库'] is not None:
                textInput.select_by_index('仓库', input['仓库'], 1)
            if input['外部编号'] is not None:
                textInput.input_by_label('外部编号',input['外部编号'])
            textInput.special_input("客户", "SHA", "SHAPGJHWYS/上海永旭集装箱运输")
            self.click('xpath',"//input[@placeholder='选择计划提货日期']")
            self.click('xpath',"//button[@class='el-button el-picker-panel__link-btn el-button--default el-button--mini is-plain']")
            textInput.special_input("船名", "TOLTEN", "TOLTEN")
            self.waitloading()
            textInput = text(self.driver)
            textInput.input_by_label('航次',input['航次'])
            textInput.input_by_label('联系人',input['联系人'])
            textInput.input_by_label('联系电话',input['联系电话'])
            textInput.get_element('xpath',"//textarea[@placeholder='请输入备注']").send_keys(input['备注'])
            self.save_and_close()
            createTime = DataTime.GetTime()
            self.logger.info('check1：验证添加主计划弹出提示信息')
            self.check_alert_and_close(input["addplanalert"])
        except:
            self.click("x", "//button//span[text()='取消 ']")
        tableCheck = Table(self.driver,2)
        self.logger.info('check2：验证添加后列表的值正确')
        config.bulkoutNumber = tableCheck.get_value("计划号")
        self.logger.info("散货出库计划号:" + config.bulkoutNumber)
        check.is_in(tableCheck.get_value("计划类型"), input['计划类型'])
        check.equal(tableCheck.get_value("客户"), "上海永旭集装箱运输")
        tableCheck1 = Table(self.driver)
        check.is_in(tableCheck1.get_value("堆场"), input['堆场'])
        check.is_in(tableCheck1.get_value("仓库"), input['仓库'])
        check.equal(tableCheck1.get_value("外部编号"), input['外部编号'])
        check.is_in(tableCheck1.get_value("船名"), 'TOLTEN')
        check.equal(tableCheck1.get_value("航次"), input['航次'])
        check.equal(tableCheck1.get_value("联系人"), input['联系人'])
        check.equal(tableCheck1.get_value("联系电话"), input['联系电话'])
        check.equal(tableCheck1.get_value("备注"), input['备注'])
        check.less(DataTime.get_dif_time(tableCheck1.get_value("创建时间"), createTime), 300)
        check.equal(tableCheck1.get_value("创建人"), config.createName)

    def addBox(self,input):
        """
        新增出库箱子
        """
        try:
            self.logger.info('散货出库计划：添加箱子')
            self.click_by_index('xpath',"//div[@id='add']",1)
            self.waitloading()
            textInput = text(self.driver)
            textInput.select_by_index('堆场',input['堆场'])
            self.click_by_index('xpath',"//span[text()='检索']",1)
            table = Table(self.driver,8)
            row = self.rows(4)
            table.tick_off_box(row)
            self.click('xpath',"//span[text()='确认']")
            self.logger.info('check1：验证添加主计划弹出提示信息')
            self.check_alert_and_close(input["addboxalert"])
        except:
            self.click("x", "//button//span[text()='取消']")

    def rows(self,index):
        """
        通过对列表循环，查找对应计划所在行数
        """
        pax = []
        att = []
        # 根据table xpath定位到表格
        table = self.get_elements('xpath',
                                  '//*[@id="app"]/div[3]/section/div[1]/div[2]/div[1]/div/div[2]/div/div/div[2]/div[1]/div[2]/table')
        # 通过标签名获取表格的所有行
        table_tr_list = self.get_elements('xpath', f"(//div[@class='vxe-table--main-wrapper'])[{index}]//tr")
        #  按行查询表格的数据，取出的数据是一整行，按,分隔每一列的数据
        for tr in table_tr_list:
            att = (tr.text).split("\n")
            pax.append(att)
        for i in pax:
            if config.bulkintoNumber in i:
                return i[0]

    def addCar(self,input):
        """
        新增车辆信息
        """
        try:
            self.logger.info('散货出库计划：添加车辆')
            self.click_by_index('xpath',"//div[@id='add']",1)
            self.waitloading()
            textInput = text(self.driver)
            if input['车牌'] is not None:
                textInput.select_by_label("车牌", input['车牌'])
            if input['车号'] is not None:
                self.get_element('xpath', "//input[@placeholder='请输入车号']").send_keys(input['车号'])
            self.save_and_close()
        except:
            self.cancel()
        createTime = DataTime.GetTime()
        self.logger.info('check1：验证新增车辆信息弹出提示信息')
        self.check_alert_and_close(input["addcaralert"])
        tableCheck = Table(self.driver,6)
        self.logger.info('check2：验证添加后列表的值正确')
        check.equal(tableCheck.get_value("车牌号"), input['车牌']+input['车号'])
        check.less(DataTime.get_dif_time(tableCheck.get_value("创建时间"), createTime), 300)
        check.equal(tableCheck.get_value("创建人"), config.createName)




    def switch_car_information(self):
        """
        切换车辆信息
        """
        self.click('xpath',"//div[contains(text(),'车辆信息')]")

    def switch_box_information(self):
        """
        切换出库明细
        """
        self.click('xpath',"//div[contains(text(),'入库明细')]")

    def more_information(self,row):
        """
        ...鼠标点击
        """
        self.logger.info('步骤1：展开...')
        table= Table(self.driver,3)
        table.moreButton(row)
        time.sleep(0.5)
        self.element_wait('id','setup')


    def perform_tasks(self):
        """
        执行按钮（后期可能需要增加判断选择了是 取消 执行 关闭 等操作，给出 对应提示）
        """
        self.more_information(1)
        self.logger.info('散货出库计划：执行')
        self.click('id', 'setup')
        self.click("xpath", "//div[@class='el-message-box__btns']//span[contains(text(),'确定')]")
        self.check_alert("执行成功")
        tableCheck = Table(self.driver)
        self.logger.info('check3：验证执行按钮后计划状态变执行状态')
        check.equal(tableCheck.get_value("计划状态"), "执行")
