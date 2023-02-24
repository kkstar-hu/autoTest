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
        self.logger.info('装箱确认：输入箱号,选择状态')
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


    def addBOX_information(self,input):
        """
        新增箱货信息
        """
        self.input_boxnumber(input)
        self.retrieve()
        self.logger.info('装箱确认：新增货物信息')
        textInput = text(self.driver)
        textInput.click('xpath', "//div[@id='add']")
        textInput.click('xpath',"//div[@class='vxe-modal--box']//span[text()='检索']")
        table = Table(self.driver, 5)
        rowid=table.select_row("入库计划号",config.bulkintoNumber)
        tableinput = Table(self.driver, 7)
        tableinput.input_by_rowid(rowid,"装箱件数",input["装箱件数"])
        tableinput.input_by_rowid(rowid, "装箱体积", input["装箱体积"])
        tableinput.input_by_rowid(rowid, "装箱重量", input["装箱重量"])
        rowid2 = table.select_row("仓库", input["车牌"]+input["车号"])
        tableinput.input_by_rowid(rowid2, "装箱件数", input["装箱件数1"])
        tableinput.input_by_rowid(rowid2, "装箱体积", input["装箱体积1"])
        tableinput.input_by_rowid(rowid2, "装箱重量", input["装箱重量1"])
        table.check("入库计划号",config.bulkintoNumber)
        table.check("仓库", input["车牌"]+input["车号"])
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
        self.logger.info('装箱确认：展开...')
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




