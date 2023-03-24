from Base.basepage import BasePage
from Commons.Controls.table import Table
from Commons.Controls.text import text
from Commons.DateTime import DataTime
import pytest_check as check
from NZYMS.config import config

class Bulk_cargo_into_storageConfirm(BasePage):
    """散货入库确认"""
    def input_carnumber(self,input):
        """ 输入车牌号"""
        self.logger.info('散货入库确认：输入车牌号')
        textInput = text(self.driver)
        textInput.input_by_placeholder('请输入车牌号',input['车牌']+input['车号'])
        textInput.select_by_label("结算主体",input['结算主体'])

    def retrieve(self):
        """点击检索按钮"""
        self.click('xpath', "//span[text()='检索']")

    def reset(self):
        """点击重置按钮 """
        self.click('xpath', "//span[text()='重置']")

    def addbulk_into(self,input):
        """新增入库登记信息"""
        try:
            self.input_carnumber(input)
            self.retrieve()
            self.logger.info('散货入库确认：新增入库信息')
            textInput = text(self.driver)
            textInput.click('xpath', "//div[@id='add']")
            textInput.select_by_placeholder_index('请选择', input['入库位置1'],1)
            textInput.select_by_placeholder_index('请选择', input['入库位置2'],2)
            textInput.input_by_number('入库/残碎件数', input['入库'],0)
            textInput.input_by_number('入库/残碎件数', input['残碎'],1)
            textInput.input_by_label('体积', input['体积'])
            textInput.input_by_label('入库重量(kg)', input['入库重量(kg)'])
            self.save_and_close()
            createTime = DataTime.GetTime()
            self.logger.info('check1：验证入库明细弹出提示信息')
            self.has_alert(input["addboxconfirm"])
        except:
            self.click("xpath", "//button//span[text()='取消 ']")
        tableCheck = Table(self.driver,2)
        self.logger.info('check3：验证添加后列表的值正确')
        check.equal(tableCheck.get_value("入库计划件数"), str(int(input['入库']) + int(input['残碎'])))
        check.equal(tableCheck.get_value("入库计划体积"), input['体积'])
        check.equal(tableCheck.get_value("入库计划重量(kg)"), input['入库重量(kg)'])
        check.equal(tableCheck.get_value("残损件数"), input['残碎'])
        check.equal(tableCheck.get_value("入库件数"), input['入库'])
        check.equal(tableCheck.get_value("入库体积"), input['入库体积'])
        check.equal(tableCheck.get_value("入库重量(kg)"), input['入库重量(kg)'])
        check.equal(tableCheck.get_value("入库位置"), input['入库位置1']+input['入库位置2'])
        check.less(DataTime.get_dif_time(createTime,tableCheck.get_value("登记时间")), 100)
        check.equal(tableCheck.get_value("登记人"), config.createName)
