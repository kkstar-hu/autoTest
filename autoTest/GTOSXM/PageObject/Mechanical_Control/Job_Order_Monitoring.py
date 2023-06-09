import time
import pytest_check as check
from Base.basepage import BasePage
from GTOSXM.Controls.text import Gtos_text
from GTOSXM.Config import config, configinterface
from GTOSXM.Controls.Gtos_table import Gtos_table


class Job_Order_Monitoring(BasePage):
    """
    作业指令监控
    """

    def Retrieve(self, input, shipname=None, boxnumber=None, carnumber=None):
        """
        输入内容，检索
        """
        self.logger.info('作业指令监控-查询')
        textinput = Gtos_text(self.driver)
        self.waitloading()
        textinput.multi_select_by_label('作业路类型', input['作业路类型'])
        if shipname is not None:
            textinput.search_select_by_label('船名航次', shipname)
        if boxnumber is not None:
            textinput.input_by_label("箱号", boxnumber)
        if carnumber is not None:
            self.click('x', "//span[text()=' 更多']")
            textinput.input_by_label('机械号', carnumber)
        self.click('xpath', "//span[text()='检索']")

    def choice_boxnumber(self,boxnumber):
        """
        输入箱号,检索
        """
        self.logger.info('作业指令监控-查询')
        textinput = Gtos_text(self.driver)
        textinput.input_by_label('箱号', boxnumber)
        self.click('xpath', "//span[text()='检索']")

    def order_info_check(self, input, boxnumber):
        """
        作业信息查验
        """
        self.logger.info('作业指令监控-校验列表数据')
        tablecheck = Gtos_table(self.driver)
        check.is_in(tablecheck.get_value('箱号').replace(' ', '').replace('\n', ''), boxnumber)
        if self.hasInput(input, '作业路'):
            check.equal(tablecheck.get_value('作业路'), input['作业路'])
        if self.hasInput(input, '操作过程'):
            check.equal(tablecheck.get_value('操作过程'), input['操作过程'])
        if self.hasInput(input, '作业方式'):
            check.equal(tablecheck.get_value('作业方式'), input['作业方式'])
        check.equal(tablecheck.get_value('箱状态'), input['箱状态'])
        check.equal(tablecheck.get_value('卸货港'), input['卸货港'])
        check.equal(tablecheck.get_value('作业状态'), '等待作业')
        check.equal(tablecheck.get_value('归属码头'), config.showname)
        if 'xm' not in config.host:  #β环境好像没有
            check.equal(tablecheck.get_value('指令归属码头'), config.showname)
        if 'xm' not in config.host:  #β环境好像没有
            check.equal(tablecheck.get_value('指令作业码头'), config.showname)
        if self.hasInput(input, '集卡编号'):
            check.equal(tablecheck.get_value('拖运机械'), input['车牌'] + input['集卡编号'])
        if self.hasInput(input, '集卡编号'):
            check.equal(tablecheck.get_value('当前位置'), input['车牌'] + input['集卡编号'])
        if self.hasInput(input, '集卡编号'):
            check.equal(tablecheck.get_value('起始位置'), input['车牌'] + input['集卡编号'])
        check.equal(tablecheck.get_value('尺寸'), input['尺寸'])
        if self.hasInput(input, '箱型check'):
            check.equal(tablecheck.get_value('箱型'), input['箱型check'])
        if self.hasInput(input, '箱高check'):
            check.equal(tablecheck.get_value('箱高'), input['箱高check'])
        if self.hasInput(input, '箱货总重(吨)'):
            check.equal(tablecheck.get_value('箱货总重(吨)'),
                        str(format(float(input['箱货总重']) * float(0.001), '.3f')))
        check.equal(tablecheck.get_value('持箱人'), input['持箱人'])

    def order_info_check_new(self, input, boxnumber):
        """
        作业信息查验
        """
        self.logger.info('作业指令监控-校验列表数据')
        tablecheck = Gtos_table(self.driver)
        self.waitloading()
        check.is_in(tablecheck.get_value('箱号').replace(' ', '').replace('\n', ''), boxnumber)
        if self.hasInput(input, '作业路'):
            check.equal(tablecheck.get_value('作业路'), input['作业路'])
        if self.hasInput(input, '操作过程'):
            check.equal(tablecheck.get_value('操作过程'), input['操作过程'])
        check.equal(tablecheck.get_value('箱状态'), input['箱状态'])
        check.equal(tablecheck.get_value('卸货港'), input['卸货港'])
        if tablecheck.get_value('作业状态') == '等待作业':
            check.equal(tablecheck.get_value('作业状态'), '等待作业')
        check.equal(tablecheck.get_value('归属码头'), config.showname)
        if 'xm' not in config.host:
            check.equal(tablecheck.get_value('指令归属码头'), config.showname)
        if 'xm' not in config.host:
            check.equal(tablecheck.get_value('指令作业码头'), config.showname)
        if self.hasInput(input, '持箱人'):
            check.equal(tablecheck.get_value('持箱人'), input['持箱人'])
        if self.hasInput(input, '箱型'):
            check.equal(tablecheck.get_value('箱型'), input['箱型'])
        if self.hasInput(input, '箱高'):
            check.equal(tablecheck.get_value('箱高'), input['箱高'])
        if self.hasInput(input, '箱货总重'):
            check.equal(tablecheck.get_value('箱货总重(吨)'),
                        str(format(float(input['箱货总重']) * float(0.001), '.3f')))
        if self.hasInput(input, '作业方式'):
            check.equal(tablecheck.get_value('作业方式'), input['作业方式'])
            if input['操作过程'] == '船―场':
                a = Gtos_table(self.driver)
                car = a.get_value('拖运机械')
                check.equal(tablecheck.get_value('起始位置'), input['作业路'])
                check.equal(tablecheck.get_value('拖运机械'), car)
                check.equal(tablecheck.get_value('当前位置'), '')
            elif input['操作过程'] == '场―车':
                check.equal(tablecheck.get_value('起始位置'), config.boxPosition)
                check.equal(tablecheck.get_value('拖运机械'), input['车牌'] + input['集卡编号'])
                check.equal(tablecheck.get_value('当前位置'), config.boxPosition)
            elif input['操作过程'] == '船―车':
                check.equal(tablecheck.get_value('起始位置'), 'AUTO')
                check.equal(tablecheck.get_value('拖运机械'), input['车牌'] + input['集卡编号'])
                check.equal(tablecheck.get_value('当前位置'), '')
            elif input['操作过程'] == '车―船':
                check.equal(tablecheck.get_value('起始位置'), input['车牌'] + input['集卡编号'])
                check.equal(tablecheck.get_value('拖运机械'), input['车牌'] + input['集卡编号'])
                check.equal(tablecheck.get_value('当前位置'), input['车牌'] + input['集卡编号'])
            elif input['操作过程'] == '车―场':
                check.equal(tablecheck.get_value('拖运机械'), input['车牌'] + input['集卡编号'])
                check.equal(tablecheck.get_value('当前位置'), input['车牌'] + input['集卡编号'])
                check.equal(tablecheck.get_value('当前位置'), input['车牌'] + input['集卡编号'])

    def dredge_check(self, boxnumber):
        """
        空箱疏运查验
        """
        self.logger.info('作业指令监控-空箱输运信息查验')
        tablecheck = Gtos_table(self.driver)
        self.waitloading()
        rowid = self.get_attribute_info('x', f"(//div[@class='ag-center-cols-container'])[1]//div[@col-id='Cntrno' and text()='{boxnumber}']//ancestor::div[@row-id]",'row-id')
        check.equal(tablecheck.get_value_by_rowid(rowid, '箱号'), boxnumber)
        check.equal(tablecheck.get_value_by_rowid(rowid, '作业方式'), '疏运')
        check.equal(tablecheck.get_value_by_rowid(rowid, '作业状态'), '等待作业')

    def selectRow_check(self, boxnumber):
        """
        多条数据查验
        """
        self.logger.info('作业指令监控-空箱输运多条信息查验')
        table = Gtos_table(self.driver)
        self.left_click('x', f"//div[text()='{boxnumber}']")
        rowid = self.get_attribute_info('x', f"(//div[@class='ag-center-cols-container'])[1]//div[@col-id='Cntrno' and text()='{boxnumber}']//ancestor::div[@row-id]",'row-id')
        check.equal(table.get_value_by_rowid(rowid, '箱号'), boxnumber)
        check.equal(table.get_value_by_rowid(rowid, '作业方式'), '疏运')
        if boxnumber == configinterface.boxNumber:
            check.equal(table.get_value_by_rowid(rowid, '作业状态'), '待退箱')
        if boxnumber == configinterface.boxNumbertwo:
            check.equal(table.get_value_by_rowid(rowid, '作业状态'), '暂停')


    def charge_car(self, input):
        """
        改配集卡
        """
        tablecheck = Gtos_table(self.driver)
        if tablecheck.get_value('作业状态') == '等待作业':
            self.logger.info('作业指令监控-改配集卡操作')
            textclick = Gtos_text(self.driver)
            textclick.no_elements_click('改配集卡')
            textclick.click('xpath', "(//div[@role='tooltip'])[1]//input[@placeholder='请选择']")
            textclick.no_elements_click(config.carnumber, 2)
            textclick.no_elements_click('保存')
            self.check_alert_and_close('改配成功!')
            check.equal(tablecheck.get_value('作业状态'), '已配集卡')
            if self.hasInput(input, '操作过程'):
                if input['操作过程'] == '船―场':
                    check.equal(tablecheck.get_value('起始位置'), input['作业路'])
                    check.equal(tablecheck.get_value('当前位置'), '')
                    check.equal(tablecheck.get_value('拖运机械'), config.carnumber)
        self.logger.info('作业指令监控-自动分配集卡')
        if self.hasInput(input, '操作过程'):
            if input['操作过程'] == '船―场':
                check.equal(tablecheck.get_value('起始位置'), input['作业路'])
                check.equal(tablecheck.get_value('当前位置'), '')
                a = Gtos_table(self.driver)
                car = a.get_value('拖运机械')
                check.equal(tablecheck.get_value('拖运机械'), car)

    def discharging_confirm(self, input):
        """
        卸船确认按钮
        """
        self.logger.info('作业指令监控-卸船确认')
        textclick = Gtos_text(self.driver)
        textclick.no_elements_click('卸船确认')
        textclick.select_by_label("桥吊司机：", 'test02')
        self.element_wait("xpath", "//div[@role='alert']//p")
        a = Gtos_table(self.driver)
        config.boxPosition = a.get_body_values('收箱位')
        self.logger.info('箱位置：' + config.boxPosition)
        carnumber = a.get_body_values('集卡号')
        self.close_alert(f"{config.boxPosition},获取收箱位成功！")
        time.sleep(1)
        textclick.click('xpath', "(//span[text()='保存'])[3]")
        time.sleep(1)
        self.check_alert('卸船确认成功')
        self.close_alert('卸船确认成功')
        tablecheck = Gtos_table(self.driver)
        check.equal(tablecheck.get_value('作业状态'), '已装车')
        if input['操作过程'] == '船―场':
            check.equal(tablecheck.get_value('起始位置'), input['作业路'])
            check.equal(tablecheck.get_value('当前位置'), carnumber)
            check.equal(tablecheck.get_value('目的位置'), config.boxPosition)

    def discharging_confirm_lifting(self, input):
        """
        直提卸船确认按钮
        """
        self.logger.info('作业指令监控-直提卸船确认')
        textclick = Gtos_text(self.driver)
        textclick.no_elements_click('卸船确认')
        textclick.select_by_label("桥吊司机：", 'test02')
        textclick.click('xpath', "//button[@class='el-button el-button--primary el-button--medium']")
        time.sleep(1)
        self.check_alert('卸船确认成功')
        self.close_alert('卸船确认成功')
        tablecheck = Gtos_table(self.driver)
        check.equal(tablecheck.get_value('作业状态'), '完成')
        if input['操作过程'] == '船―车':
            check.equal(tablecheck.get_value('起始位置'), 'AUTO')
            check.equal(tablecheck.get_value('拖运机械'), input['车牌'] + input['集卡编号'])
            check.equal(tablecheck.get_value('当前位置'), input['车牌'] + input['集卡编号'])

    def LadeShip_confirm(self, input):
        """
        装船确认按钮
        """
        self.logger.info('作业指令监控-装船确认')
        textclick = Gtos_text(self.driver)
        textclick.no_elements_click('装船确认')
        textclick.select_by_label("桥吊司机：", input["桥吊司机"])
        textclick.select_by_label("特殊：", input["特殊"])
        textclick.click('xpath', "//span[text()='保 存']")
        self.check_alert(input['alert'])

    def closed_box(self, input):
        """
        堆场收箱
        """
        self.logger.info('作业指令监控-堆场收箱')
        textclick = Gtos_text(self.driver)
        textclick.no_elements_click('堆场收箱')
        textclick.select_by_label("堆场司机：", input["堆场司机"])
        textclick.select_by_label("作业机械：", input["作业机械"])
        textclick.click('xpath', "(//span[text()='保存'])[3]")
        self.check_alert('作业完成')
        self.close_alert('作业完成')

    def send_box(self, input):
        """
        堆场发箱
        """
        self.logger.info('作业指令监控-堆场发箱')
        textclick = Gtos_text(self.driver)
        self.click('xpath', "//span[text()='堆场发箱']")
        textclick.select_by_label("堆场司机：", input["堆场司机"])
        textclick.select_by_label("作业机械：", input["作业机械"])
        textclick.click('xpath', "(//span[text()='保存'])[3]")
        self.check_alert('作业完成')
        self.close_alert('作业完成')
        tablecheck = Gtos_table(self.driver)
        check.equal(tablecheck.get_value('作业状态'), input["作业状态"])
        if self.hasInput(input, '操作过程'):
            if input['操作过程'] == '场―车':
                check.equal(tablecheck.get_value('当前位置'), input['车牌'] + input['集卡编号'])

    def shipping_confirmation(self, input):
        """
        装船确认
        """
        self.logger.info('作业指令监控-装船确认')
        textclick = Gtos_text(self.driver)
        self.click('xpath', "//span[text()='装船确认']")
        textclick.select_by_label("桥吊司机：", 'test02')
        textclick.select_by_label("特殊：", '钢丝吊')
        textclick.click('xpath', "//span[text()='保 存']")
        self.check_alert('装船确认成功')
        tablecheck = Gtos_table(self.driver)
        check.equal(tablecheck.get_value('作业状态'), '完成')
        if self.hasInput(input, '操作过程'):
            if input['操作过程'] == '车―船':
                check.equal(tablecheck.get_value('起始位置'), input['车牌'] + input['集卡编号'])
                check.equal(tablecheck.get_value('拖运机械'), input['车牌'] + input['集卡编号'])
                check.equal(tablecheck.get_value('当前位置'), 'AUTO')
