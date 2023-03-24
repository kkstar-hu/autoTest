import pytest_check as check
from Base.basepage import BasePage
from Commons.Controls.table import Table
from Commons.Controls.text import text
from NZYMS.config import config


class Out_Storage_Query(BasePage):
    """出库查询"""
    def search_and_check(self,input,number):
        """
        选择结算主体、出库计划号并检索
        """
        self.logger.info('入库查询：输入结算主体并检索')
        textInput = text(self.driver)
        textInput.click('xpath',"//span[text()='更多']")
        textInput.select_by_label('结算主体',input['结算主体'])
        textInput.input_by_label('计划号',number)
        self.waitloading()
        self.click('xpath',"//span[text()='检索']")
        tableCheck = Table(self.driver, 2)
        check.is_in(tableCheck.get_value("结算主体"), input['结算主体'])
        check.is_in(tableCheck.get_value("堆场"), input['堆场'])
        check.is_in(tableCheck.get_value("仓库"), input['仓库'])
        check.equal(tableCheck.get_value("生成方式"), input['生成方式'])
        tableCheck1 = Table(self.driver)
        check.equal(tableCheck1.get_value("客户"), "上海永旭集装箱运输")
        check.equal(tableCheck1.get_value("货名"), input['货名'])
        check.equal(tableCheck1.get_value("唛头"), input['唛头'])
        check.equal(tableCheck1.get_value("包装"), input['包装'])
        check.equal(tableCheck1.get_value("出库件数"), input['出库件数check'])
        check.equal(tableCheck1.get_value("出库体积"), input['出库体积check'])
        check.equal(tableCheck1.get_value("出库重量(kg)"), input['出库重量(kg)check'])
        check.equal(tableCheck1.get_value("计划出库件数"), input['出库件数'])
        check.equal(tableCheck1.get_value("计划出库体积"), input['出库体积'])
        check.equal(tableCheck1.get_value("计划出库重量(kg)"), input['出库重量(kg)'])
        check.equal(tableCheck1.get_value("车牌号"), input['车牌'] + input['车号'])
        check.is_in(tableCheck1.get_value("计划类型"), input['计划类型'])
        check.equal(tableCheck1.get_value("外部编号"), input['外部编号'])
        check.is_in(tableCheck1.get_value("船名"), 'TOLTEN')
        check.equal(tableCheck1.get_value("航次"), input['航次'])
        check.equal(tableCheck1.get_value("登记人"), config.createName)










