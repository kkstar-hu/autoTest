import pytest_check as check
from Base.basepage import BasePage
from Commons.Controls.table import Table
from Commons.Controls.text import text
from Commons.DateTime import DataTime
from NZYMS.config import config

class Input_Check_Info(BasePage):
    """
    查验计划
    """
    def editPlan(self,input,boxnumber):
        """
        新增查验计划
        """
        try:
            self.logger.info('查验计划录入：查验录入信息')
            self.click("xpath", "(//button//span[text()='检索'])[1]")
            tablefixed = Table(self.driver,2)
            tablefixed.click_edit("查验计划号",config.checkplanNumber)
            textInput = text(self.driver)
            if input["劳务公司"] != None:
                textInput.select_by_label("劳务公司", input['劳务公司'])
            if input["掏箱方式"] != None:
                textInput.select_by_label("掏箱方式", input['掏箱方式'])
            if input["查验单位"] != None:
                textInput.select_by_label("查验单位", input['查验单位'])
            if input["是否消毒"] != None:
                textInput.select_by_label("是否消毒", input['是否消毒'])
            if input["立方数"] != None:
                textInput.input_by_label("立方数", input['立方数'])
            if input["称重次数"] != None:
                textInput.input_by_label("称重次数", input['称重次数'])
            if input["是否施封"] != None:
                textInput.select_by_label("是否施封", input['是否施封'])
            if input["是否拖车"] != None:
                textInput.select_by_label("是否拖车", input['是否拖车'])
            if input["是否熏蒸"] != None:
                textInput.select_by_label("是否熏蒸", input['是否熏蒸'])
            if input["是否开箱门"] != None:
                textInput.select_by_label("是否开箱门", input['是否开箱门'])
            if input["是否延查"] != None:
                textInput.select_by_label("是否延查", input['是否延查'])
            if input["人力装卸费"] != None:
                textInput.select_by_label("人力装卸费", input['人力装卸费'])
            if input["叉车工"] != None:
                textInput.input_by_label("叉车工", input['叉车工'])
            if input["备注"] != None:
                textInput.textarea_by_label("备注", input['备注'])
            self.save_and_close()
        except:
            self.cancel()
            createTime = DataTime.GetTime()
            self.logger.info('check1：验证提示信息')
            self.check_alert(input["alert"])
            if input["alert"]=="修改成功":
                tableCheck = Table(self.driver)
                self.logger.info('check3：验证修改后列表的值正确')
                check.equal(tableCheck.get_value("尺寸"), input['尺寸'])
                check.is_in(tableCheck.get_value("箱型"), input['箱型'])
                check.equal(tableCheck.get_value("箱高"), input['箱高'])
                check.equal(tableCheck.get_value("计划状态"), "查验中")
                check.equal(tableCheck.get_value("人力装卸费"), input['人力装卸费'])
                check.equal(tableCheck.get_value("叉车工"), input['叉车工'])
                check.equal(tablefixed.get_value("计划类型"), input['计划类型'])
                check.equal(tableCheck.get_value("是否延查"), input['是否延查'])
                check.equal(tableCheck.get_value("是否开箱门"), input['是否开箱门'])
                check.equal(tableCheck.get_value("是否拖车"), input['是否拖车'])
                check.equal(tableCheck.get_value("是否施封"), input['是否施封'])
                check.is_in(tableCheck.get_value("掏箱方式"), input['掏箱方式'])
                check.equal(tableCheck.get_value("查验单位"), input['查验单位'])
                check.equal(tableCheck.get_value("是否熏蒸"), input['是否熏蒸'])
                check.equal(tableCheck.get_value("备注"), input['备注'])
                check.equal(tableCheck.get_value("是否消毒"), input['是否消毒'])
                check.equal(tableCheck.get_value("立方数"), input['立方数'])
                check.equal(tableCheck.get_value("称重次数"), input['称重次数'])
                check.less(DataTime.get_dif_time(tableCheck.get_value("录入时间"), createTime), 300)
                check.equal(tableCheck.get_value("录入人"), config.createName)

