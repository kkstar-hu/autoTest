import time
import pytest_check as check
from Base.basepage import BasePage
from Commons.Controls.tag import Tag
from Commons.Controls.text import text
from Commons.Controls.table import Table
from Commons.menu import Menu
from NZYMS.Config import config
from NZYMS.PageObject.CrossingManagement.cars_registration import Cars_Registration
from NZYMS.PageObject.CrossingManagement.Out_confirm import Out_Confirm
from NZYMS.PageObject.MarketingDepartmentManagement.Send_Mention_CarOut import Send_Mention_CarOut


class Packing_Confirm(BasePage):
    """
    装箱计划确认
    """
    def input_boxnumber(self,input):
        """
        输入箱号
        """
        self.logger.info('步骤1：输入箱号,选择状态')
        textInput = text(self.driver)
        textInput.input_by_placeholder('请输入箱号',config.boxNumberOutPlan)
        textInput.select_by_label('装箱状态',input['装箱状态'])
        textInput.select_by_index('结算主体', input['结算主体'], 0)

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
        table_tr_list = self.get_elements('xpath',f"(//table[@class='vxe-table--body'])[{index}]//tr")
        # 通过标签名获取表格的所有行
        table = self.get_elements('xpath',"//tr")

        #  按行查询表格的数据，取出的数据是一整行，按,分隔每一列的数据
        for tr in table_tr_list:
            att = (tr.text).split("\n")
            pax.append(att)
        for i in pax:
            a.append(i)
        return a
        # c = dict(zip(a[7],a[8]))
        # c['体积'] = a[8][8]



    def addBOX_information(self,input):
        """
        新增箱货信息
        """
        self.input_boxnumber(input)
        self.retrieve()
        self.logger.info('步骤2：新增货物信息')
        textInput = text(self.driver)
        textInput.click('xpath', "//div[@id='add']")
        textInput.click('xpath',"//div[@class='vxe-modal--box']//span[text()='检索']")
        b = self.get_information(5)
        table = Table(self.driver, 6)
        for i in b:
            if '库内货' in i:
                print(i)
                print(b.index(i))
                table.tick_off_box(b.index(i)+1)
                table1 = Table(self.driver, 7)
                table1.input_by_row('装箱件数', i[7],b.index(i)+1)
                table1.input_by_row('装箱体积', i[9],b.index(i)+1)
                table1.input_by_row('装箱重量', i[8],b.index(i)+1)
            if '直装货' in i:
                print(i)
                print(b.index(i))
                table.tick_off_box(b.index(i)+1)
                table1 = Table(self.driver, 7)
                table1.input_by_row('装箱件数', i[6],b.index(i)+1)
                table1.input_by_row('装箱体积', i[8],b.index(i)+1)
                table1.input_by_row('装箱重量', i[7],b.index(i)+1)
        self.click('xpath',"//button//span[contains(text(),'确认')]")
        time.sleep(1)
        tableCheck = Table(self.driver,2)
        self.logger.info('check2：添加箱货信息后装箱状态')
        check.equal(tableCheck.get_value("装箱状态"), "初始")
        #直装货和库内货都有的情况，不会有开始装箱这个状态
        # check.equal(tableCheck.get_value("装箱状态"), "开始装箱")
        table2 = Table(self.driver, 3)
        table2.moreButton(1)
        table2.menu_complete()
        self.click("xpath","//div[@class='el-message-box__btns']//span[contains(text(),'确定')]")
        self.waitloading()
        self.logger.info('check3：点击完成后装箱状态')
        check.equal(tableCheck.get_value("装箱状态"),"装箱完成")
        self.check_alert(input["confirmalert"])

    def more_information(self,input):
        """
        ...鼠标点击
        """
        self.logger.info('步骤1：展开...')
        table = Table(self.driver,3)
        table.moreButton()
        self.element_wait('xpath',"//span[text()='完成']")
        table.menu_complete()
        self.click("xpath", "//div[@class='el-message-box__btns']//span[contains(text(),'确定')]")
        self.waitloading()
        self.logger.info('check3：点击完成后装箱状态')
        tableCheck = Table(self.driver)
        check.equal(tableCheck.get_value("装箱状态"),"装箱完成")
        self.check_alert(input["confirmalert"])


    def choice_process(self,input):
        """
        装箱计划有直装和库内装，直装需要车辆进场，放行，出场而库内装不需要
        """
        if input['新增货物方式'] == '新增':
            menu = Menu(self.driver)
            menu.select_level_Menu("道口管理,车辆进场登记")
            car_process = Cars_Registration(self.driver)
            car_process.into_process(input)
            Tag(self.driver).closeTag("车辆进场登记")
            menu.select_level_Menu("市场部管理,装箱管理,装箱确认")
            self.addBOX_information(input)
            self.more_information(input)
            Tag(self.driver).closeTag("装箱确认")
            menu.select_level_Menu("市场部管理,送提货车放行确认")
            send_and_mention = Send_Mention_CarOut(self.driver)
            send_and_mention.process(input)
            Tag(self.driver).closeTag("送提货车放行确认")
            menu.select_level_Menu("道口管理,出场确认")
            out_confirm = Out_Confirm(self.driver)
            out_confirm.out_confirm(input)
            out_confirm.choice_car(input)
            out_confirm.confirm_button()
            Tag(self.driver).closeTag("出场确认")
        else:
            menu = Menu(self.driver)
            menu.select_level_Menu("市场部管理,装箱管理,装箱确认")
            self.addBOX_information(input)
            Tag(self.driver).closeTag("装箱确认")




