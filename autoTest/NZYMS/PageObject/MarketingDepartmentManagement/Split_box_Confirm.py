import time
import pytest_check as check
from selenium.webdriver.common.by import By

from Base.basepage import BasePage
from Commons.Controls.tag import Tag
from Commons.Controls.text import text
from Commons.Controls.table import Table
from Commons.menu import Menu
from NZYMS.Config import config
from NZYMS.PageObject.CrossingManagement.cars_registration import Cars_Registration
from NZYMS.PageObject.CrossingManagement.Out_confirm import Out_Confirm
from NZYMS.PageObject.MarketingDepartmentManagement.Send_Mention_CarOut import Send_Mention_CarOut


class Split_Box_Confirm(BasePage):
    """
    拆箱计划确认
    """
    def input_boxnumber(self,input):
        """
        输入箱号
        """
        self.logger.info('步骤1：输入箱号,选择状态')
        textInput = text(self.driver)
        textInput.input_by_placeholder('请输入箱号',config.boxNumberOutPlan)
        textInput.select_by_index('结算主体', input['结算主体'], 0)
        textInput.select_by_label('拆箱状态',input['拆箱状态'])

    def retrieve(self):
        """
        点击检索按钮
        """
        self.click('xpath', "//span[text()='检索']")

    def reset(self):
        """
        点击重置按钮
        """
        self.click('xpath', "//span[text()='重置']")

    def get_information(self,index=1):
        """
        通过对列表循环，查找箱子信息
        结合成字典返回
        """
        pax = []
        att = []
        a = []
        # 根据table xpath定位到表格
        #table = self.get_elements('xpath','//*[@id="app"]/div[3]/section/div[1]/div[2]/div/div[2]/div/div[1]/div[2]/div[1]/div[2]/table')
        table = self.get_elements('xpath',f"(//div[@class='vxe-table--body-wrapper body--wrapper'])[{index}]//tr")
        # 通过标签名获取表格的所有行
        table_tr_list = self.get_elements('xpath',"//tr")

        #  按行查询表格的数据，取出的数据是一整行，按,分隔每一列的数据
        for tr in table_tr_list:
            att = (tr.text).split("\n")
            pax.append(att)
        for i in pax:
            a.append(i)
        b =dict(zip(a[-6],a[-5]))
        return b


    def switch_split_information(self):
        """
        切换拆箱车提
        """
        self.click('xpath',"//div[contains(text(),'拆箱车提')]")

    def switch_split_warehouse(self):
        """
        切换拆箱入库
        """
        self.click('xpath',"//div[contains(text(),'拆箱入库')]")



    def addBOX_information(self,input):
        """
        新增箱货信息
        """
        try:
            self.input_boxnumber(input)
            self.retrieve()
            self.logger.info('步骤2：新增货物信息')
            textInput = text(self.driver)
            textInput.click('xpath', "//div[@id='add']")
            self.refresh()
            self.input_boxnumber(input)
            self.retrieve()
            self.logger.info('步骤2：新增货物信息')
            textInput.click('xpath', "//div[@id='add']")
            textInput.select_by_placeholder('请选择堆场',input['堆场'])
            # textInput.select_by_placeholder('请选择计划类型',input['计划类型'])
            textInput.select_by_placeholder('请选择仓库',input['仓库'])
            b = self.get_information(6)
            table = Table(self.driver, 12)
            table.tick_off_box(1)
            table1 = Table(self.driver, 13)
            table1.input_by_row('拆箱件数',b['件数'])
            table1.input_by_row('拆箱体积',b['体积'])
            table1.input_by_row('拆箱重量',b['重量'])
            textInput.select_by_placeholder_index('请选择', input['入库位置1'],2)
            textInput.select_by_placeholder_index('请选择', input['入库位置2'],3)
            self.click('xpath',"//button//span[contains(text(),'确认')]")
            tableCheck = Table(self.driver,2)
            self.logger.info('check2：添加箱货信息后装箱状态')
            check.equal(tableCheck.get_value("拆箱状态"), "开始拆箱")
            self.switch_split_information()
            textInput.click('xpath', "//div[@id='add']")
            table2 = Table(self.driver, 14)
            table2.tick_off_box(1)
            table2.input_by_row('拆箱件数',b['件数'])
            table2.input_by_row('拆箱体积',b['体积'])
            table2.input_by_row('拆箱重量',b['重量'])
            self.click_by_index('xpath',"//button//span[contains(text(),'确认')]",1)
            table3 = Table(self.driver, 3)
            table3.moreButton(1)
            table3.menu_complete()
            self.element_wait_disappear(By.XPATH, "//div[@role='alert']//p")
            self.click("xpath","//div[@class='el-message-box__btns']//span[contains(text(),'确定')]")
            self.waitloading()
            self.logger.info('check3：点击完成后装箱状态')
            check.equal(tableCheck.get_value("拆箱状态"),"完成拆箱")
            self.check_alert(input["confirmalert"])
        except:
            self.cancel()








