from Base.basepage import BasePage
from GTOS.Controls.Gtos_table import Gtos_table
from GTOS.Controls.text import Gtos_text
from GTOS.Config import config


class PlanManagement(BasePage):
    """
    计划受理--计划管理
    """
    def select_value(self, boxnumber):
        """
        输入船名航次
        """
        self.logger.info('计划管理-查询：输入船名航次')
        textinput = Gtos_text(self.driver)
        textinput.search_select_by_label('船名航次', config.importNumber)
        textinput.input_by_label('箱号', boxnumber)
        self.click('xpath', "//span[text()='检索']")

    def viewing_Plan(self):
        """
        查看计划
        """
        self.logger.info('计划管理-查看计划')
        self.click('xpath', "//div//span[text()='查看计划']")
        table = Gtos_table(self.driver)
        config.Number = table.plan_get_value('箱预约号')
