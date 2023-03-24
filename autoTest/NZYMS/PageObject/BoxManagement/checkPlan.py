import pytest_check as check
from Base.basepage import BasePage
from Commons.Controls.el_table import ELtable
from Commons.Controls.table import Table
from Commons.Controls.text import text
from Commons.DateTime import DataTime
from NZYMS.config import config

class Check_Plan(BasePage):

    def addcheckPlan(self,input):
        """
        新增查验计划
        """
        try:
            self.logger.info('查验计划：添加查验计划')
            self.click("xpath", "(//div[@id='add'])[1]")
            textInput = text(self.driver)
            self.logger.info('check1：验证查验计划号和查验方式不可编辑')
            check.is_false(textInput.text_isenable("查验计划号",index=0))
            check.is_false(textInput.text_isenable("查验方式",index=0))
            if input["堆场"] != None:
                textInput.select_by_index("堆场", input['堆场'])
            textInput.special_input("申请客户", "SHA", "SHAPGJHWYS/上海永旭集装箱运输")
            textInput.special_input("结算客户", "SHA", "SHAPGJHWYS/上海永旭集装箱运输")
            if input["计划类型"] != None:
                textInput.select_by_index("计划类型", input['计划类型'])
            if input["计划开始时间"] != None:
                textInput.input_by_label("计划开始时间", input['计划开始时间'])
            if input["计划结束时间"] != None:
                textInput.input_by_label("计划结束时间", input['计划结束时间'])
            if input["联系电话"] != None:
                textInput.input_by_label("联系电话", input['联系电话'])
            if input["查验科室"] != None:
                textInput.select_by_index("查验科室", input['查验科室'])
            if input["查验单位"] != None:
                textInput.select_by_label("查验单位", input['查验单位'])
            if input["联系人"] != None:
                textInput.input_by_label("联系人", input['联系人'])
            if input["备注"] != None:
                textInput.input_by_label("备注", input['备注'])
            self.save_and_close()
            createTime = DataTime.GetTime()
            self.logger.info('check2：验证提示信息')
            self.check_alert_and_close(input["addplanalert"])
        except:
            self.click("x","//button//span[text()='取消 ']")
        if input["addplanalert"]=="新增成功":
            tableCheckfixed = Table(self.driver,2)
            self.logger.info('check3：验证添加后列表的值正确')
            config.checkplanNumber = tableCheckfixed.get_value("计划号")
            check.equal(tableCheckfixed.get_value("计划类型"), input['计划类型'])
            tableCheck = Table(self.driver)
            check.equal(tableCheck.get_value("堆场"), input['堆场'])
            check.equal(tableCheck.get_value("计划状态"), "计划")
            check.equal(tableCheck.get_value("申请客户"), "上海永旭集装箱运输")
            check.equal(tableCheck.get_value("结算客户"), "上海永旭集装箱运输")
            check.is_in(tableCheck.get_value("查验科室"), input['查验科室'])
            check.is_in(tableCheck.get_value("查验单位"), input['查验单位'])
            check.equal(tableCheck.get_value("是否再生品"), input['是否再生品'])
            check.equal(tableCheck.get_value("是否放射性"), input['是否放射性'])
            check.equal(tableCheck.get_value("是否加急"), input['是否加急'])
            check.equal(tableCheck.get_value("是否熏蒸"), input['是否熏蒸'])
            check.equal(tableCheck.get_value("备注"), input['备注'])
            check.equal(tableCheck.get_value("联系电话"), input['联系电话'])
            check.equal(tableCheck.get_value("联系人"), input['联系人'])
            check.less(DataTime.get_dif_time(createTime,tableCheck.get_value("创建时间")), 100)
            check.equal(tableCheck.get_value("创建人"), config.createName)

    def addWorkOrder(self, input, boxNumber):
        try:
            self.logger.info('查验计划添加箱：添加作业指令')
            self.click("xpath","(//div[@id='add'])[2]")
            textInput = text(self.driver)
            textInput.input_by_placeholder("请输入箱号", boxNumber)
            textInput.select_by_index("堆场", input['堆场'])
            self.click("xpath", "(//button//span[text()='检索'])[2]")
            tableCheck = ELtable(self.driver)
            self.logger.info('check4：验证添加作业指令窗口中列表的值正确')
            check.is_in(tableCheck.get_value_by_trElement("箱号",boxNumber,"堆场"), input['堆场'])
            check.equal(tableCheck.get_value_by_trElement("箱号",boxNumber,"箱号"), boxNumber)
            check.equal(tableCheck.get_value_by_trElement("箱号",boxNumber,"尺寸"), input['尺寸'])
            check.is_in(tableCheck.get_value_by_trElement("箱号",boxNumber,"箱型"), input['箱型'])
            check.equal(tableCheck.get_value_by_trElement("箱号",boxNumber,"箱高"), input['箱高'])
            check.equal(tableCheck.get_value_by_trElement("箱号",boxNumber,"箱状态"), "已落箱")
            tableCheck.select_row("箱号",boxNumber)
            self.click("xpath", "//button//span[contains(text(),'确认')]")
            self.click("xpath", "//span[text()='保存']")
            self.check_alert(input["alert"])
        except:
            self.cancel()

    def clickExcute(self, row):
        table = Table(self.driver, 3)
        table.excuteButton(row)
        self.click("xpath", "//div[@class='el-message-box__btns']//span[contains(text(),'确定')]")
        self.has_alert("计划状态修改成功")
        tableCheck = Table(self.driver)
        self.logger.info('check3：验证执行按钮后计划状态变执行状态')
        check.equal(tableCheck.get_value("计划状态"), "计划")