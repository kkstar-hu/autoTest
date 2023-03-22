from Base.basepage import BasePage
from Commons.Controls.table import Table
from Commons.Controls.text import text
from NZYMS.Config import config


class Storage_Box_Query(BasePage):
    """
    存场箱查询页面操作
    """
    def select_body(self,input):
        """
        选择结算主体并检索
        """
        self.logger.info('步骤1：输入结算主体并检索')
        textInput = text(self.driver)
        textInput.click('xpath',"//span[text()='更多']")
        if input['结算主体'] is not None:
            textInput.select_by_label('结算主体',input['结算主体'])
        if input['箱号'] is not None:
            textInput.input_by_label('箱号',config.boxNumberOutPlan)
        self.waitloading()
        self.click('xpath',"//span[text()='检索']")










