
import pytest_check as check
from Base.basepage import BasePage
from GTOS.Controls.text import Gtos_text
from GTOS.Config import config
from GTOS.Controls.Gtos_table import Gtos_table


class Job_Order_Monitoring(BasePage):
    """
    作业指令监控
    """

    def Retrieve(self,input,shipNumber=None,boxnumber=None):
        """
        输入内容，检索
        """
        self.logger.info('步骤1：作业指令，输入航名航次')
        textinput = Gtos_text(self.driver)
        textinput.multi_select_by_label('作业路类型',input['作业路类型'])
        if shipNumber != None:
            textinput.search_select_by_label('船名航次',shipNumber)
        if boxnumber!=None:
            textinput.input_by_label("箱号",boxnumber)
        self.logger.info('步骤2：检索')
        self.click('xpath',"//span[text()='检索']")


    def order_info_check(self,input,boxnumber):
        """
        作业信息查验
        """
        self.logger.info('步骤3：校验内容')
        tablecheck = Gtos_table(self.driver)
        check.is_in(tablecheck.get_value('箱号').replace(' ', '').replace('\n', ''), boxnumber)
        if self.hasInput(input,'作业路'):
            check.equal(tablecheck.get_value('作业路'), input['作业路'])
        if self.hasInput(input, '操作过程'):
            check.equal(tablecheck.get_value('操作过程'), input['操作过程'])
        if self.hasInput(input, '作业方式'):
            check.equal(tablecheck.get_value('作业方式'), input['作业方式'])
        check.equal(tablecheck.get_value('箱状态'), input['箱状态'])
        check.equal(tablecheck.get_value('卸货港'), input['卸货港'])
        check.equal(tablecheck.get_value('作业状态'), '等待作业')
        if self.hasInput(input, '集卡编号'):
            check.equal(tablecheck.get_value('拖运机械'), input['车牌'] + input['集卡编号'])
        if self.hasInput(input, '当前位置'):
            check.equal(tablecheck.get_value('当前位置'),input['车牌']+input['集卡编号'])
        if self.hasInput(input, '当前位置系统'):
            check.equal(tablecheck.get_value('当前位置'), boxPosition)
        if self.hasInput(input, '起始位置'):
            check.equal(tablecheck.get_value('起始位置'),input['车牌']+input['集卡编号'])
        if self.hasInput(input, '起始位置系统'):
            check.equal(tablecheck.get_value('起始位置'), boxPosition)
        check.equal(tablecheck.get_value('尺寸'), input['尺寸'])
        if self.hasInput(input, '箱型check'):
            check.equal(tablecheck.get_value('箱型'), input['箱型check'])
        if self.hasInput(input, '箱高check'):
            check.equal(tablecheck.get_value('箱高'), input['箱高check'])
        if self.hasInput(input, '箱货总重(吨)'):
            check.equal(tablecheck.get_value('箱货总重(吨)'), str(format(float(input['箱货总重']) * float(0.001), '.3f')))
        check.equal(tablecheck.get_value('持箱人'), input['持箱人'])

    def order_Direct_lifting_check(self,input,boxnumber):
        """
        直提查验
        """
        self.logger.info('步骤3：校验内容')
        tablecheck = Gtos_table(self.driver)
        check.is_in(tablecheck.get_value('箱号').replace(' ', '').replace('\n', ''), boxnumber)
        if self.hasInput(input,'作业路'):
            check.equal(tablecheck.get_value('作业路'), input['作业路'])
        if self.hasInput(input, '操作过程'):
            check.equal(tablecheck.get_value('操作过程'), input['操作过程'])
        if self.hasInput(input, '作业方式'):
            check.equal(tablecheck.get_value('作业方式'), input['作业方式'])
        check.equal(tablecheck.get_value('箱状态'), input['箱状态'])
        check.equal(tablecheck.get_value('卸货港'), input['卸货港'])
        check.equal(tablecheck.get_value('作业状态'), '等待作业')
        if self.hasInput(input, '集卡编号'):
            check.equal(tablecheck.get_value('拖运机械'), input['车牌'] + input['集卡编号'])
        if self.hasInput(input, '集卡编号'):
            check.equal(tablecheck.get_value('当前位置'),'')
        if self.hasInput(input, '集卡编号'):
            check.equal(tablecheck.get_value('起始位置'),'B109')
        check.equal(tablecheck.get_value('尺寸'), input['尺寸'])
        if self.hasInput(input, '箱型check'):
            check.equal(tablecheck.get_value('箱型'), input['箱型check'])
        if self.hasInput(input, '箱高check'):
            check.equal(tablecheck.get_value('箱高'), input['箱高check'])
        if self.hasInput(input, '箱货总重(吨)'):
            check.equal(tablecheck.get_value('箱货总重(吨)'), str(format(float(input['箱货总重']) * float(0.001), '.3f')))
        check.equal(tablecheck.get_value('持箱人'), input['持箱人'])
    def selectRow(self):
        table = Gtos_table(self.driver)
        table.select_row("箱号",config.boxNumber)

    def charge_car(self,car):
        """
        改配集卡
        """
        self.logger.info('步骤1：改配集卡操作')
        textclick = Gtos_text(self.driver)
        textclick.no_elements_click('改配集卡')
        textclick.click('xpath',"(//div[@role='tooltip'])[1]//input[@placeholder='请选择']")
        textclick.no_elements_click(car,2)
        textclick.no_elements_click('保存')
        self.check_alert_and_close('改配成功!')
        self.logger.info('步骤2：校验内容')
        tablecheck = Gtos_table(self.driver)
        check.equal(tablecheck.get_value('作业状态'), '已配集卡')

    def discharging_confirm(self):
        """
        卸船确认按钮
        """
        self.logger.info('步骤1：卸船确认')
        textclick = Gtos_text(self.driver)
        textclick.no_elements_click('卸船确认')
        textclick.input_noclear_placeholder_click('请选择','HAS',5)
        a = Gtos_table(self.driver)
        global boxPosition
        boxPosition= a.get_body_values('收箱位')
        self.close_alert(f"{a.get_body_values('收箱位')},获取收箱位成功！")
        textclick.click('xpath',"(//span[text()='保存'])[3]")
        self.check_alert('卸船确认成功')
        self.close_alert('卸船确认成功')
        self.logger.info('步骤2：校验内容')
        tablecheck = Gtos_table(self.driver)
        check.equal(tablecheck.get_value('作业状态'), '已装车')

    def discharging_confirm_lifting(self):
        """
        直提卸船确认按钮
        """
        self.logger.info('步骤1：卸船确认')
        textclick = Gtos_text(self.driver)
        textclick.no_elements_click('卸船确认')
        textclick.input_noclear_placeholder_click('请选择','HAS',5)
        a = Gtos_table(self.driver)
        textclick.click('xpath',"(//span[text()='保存'])[3]")
        self.check_alert('卸船确认成功')
        self.close_alert('卸船确认成功')
        self.logger.info('步骤2：校验内容')
        tablecheck = Gtos_table(self.driver)
        check.equal(tablecheck.get_value('作业状态'), '完成')



    def LadeShip_confirm(self,input):
        """
        装船确认按钮
        """
        self.logger.info('步骤1：装船确认')
        textclick = Gtos_text(self.driver)
        textclick.no_elements_click('装船确认')
        textclick.select_by_label("桥吊司机：",input["桥吊司机"])
        textclick.select_by_label("特殊：",input["特殊"])
        textclick.click('xpath',"//span[text()='保 存']")
        self.check_alert('作业完成')


    def closed_box(self,input):
        """
        堆场收箱
        """
        self.logger.info('步骤1：堆场收箱')
        textclick = Gtos_text(self.driver)
        textclick.no_elements_click('堆场收箱')
        textclick.select_by_label("堆场司机：", input["堆场司机"])
        textclick.select_by_label("作业机械：", input["作业机械"])
        textclick.click('xpath',"(//span[text()='保存'])[3]")
        self.check_alert('作业完成')

    def send_box(self,input):
        """
        堆场发箱
        """
        self.logger.info('步骤1：堆场发箱')
        textclick = Gtos_text(self.driver)
        self.click('xpath', "//span[text()='堆场发箱']")
        textclick.select_by_label("堆场司机：", input["堆场司机"])
        textclick.select_by_label("作业机械：", input["作业机械"])
        textclick.click('xpath',"(//span[text()='保存'])[3]")
        self.check_alert('作业完成')
        tablecheck = Gtos_table(self.driver)
        check.equal(tablecheck.get_value('作业状态'), '已装车')

    def shipping_confirmation(self):
        """
        装船确认
        """
        self.logger.info('步骤1：装船确认')
        textclick = Gtos_text(self.driver)
        self.click('xpath', "//span[text()='装船确认']")
        textclick.input_noclear_placeholder_click('请选择','HAS',5)
        textclick.input_noclear_placeholder_click('请选择','钢丝吊',6)
        textclick.click('xpath',"//span[text()='保 存']")
        self.check_alert('装船确认成功')

    def Job_DischargingOrder(self,input,boxnumber):
        """
        工作指令卸船操作流程
        """
        self.Retrieve(input)
        self.order_info_check(input,boxnumber)
        self.charge_car('A303')
        self.discharging_confirm()
        self.closed_box(input)

    def lifting_Order(self,input,boxnumber):
        """
        直提卸船确认
        """
        self.Retrieve(input,boxnumber=boxnumber)
        self.order_Direct_lifting_check(input,boxnumber)
        self.discharging_confirm_lifting()

    def Job_PackingboxOrder(self,input):
        """
        工作指令-提箱流程-装船确认
        """
        self.Retrieve(input)
        self.order_info_check(input)
        self.shipping_confirmation()

    def loading_PackingboxOrder(self,input,boxmunber):
        """
        直装
        """
        self.Retrieve(input,boxnumber=boxmunber)
        self.order_info_check(input,boxmunber)
        self.shipping_confirmation()




    def Job_SendBoxOrder(self,input,boxmunber):
        """
        工作指令-堆场发箱
        """
        self.Retrieve(input)
        self.order_Take_check(input,boxmunber)
        self.send_box(input)

