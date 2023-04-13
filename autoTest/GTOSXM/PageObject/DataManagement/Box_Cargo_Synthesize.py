
import pytest_check as check
from Base.basepage import BasePage
from GTOS.Controls.text import Gtos_text
from GTOSXM.Config import configinterface
from GTOSXM.Controls.Gtos_table import Gtos_table


class Box_Cargo_Synthesize(BasePage):
    """
    箱货综合查询
    """

    def input_values(self):
        """
        输入查询内容
        """
        self.logger.info('箱综合查询：输入内容检索信息')
        text = Gtos_text(self.driver)
        text.input_by_label('箱号', configinterface.boxNumbertwo)
        self.click('x', "//span[text()='检索']")
        self.left_click('x', "//span[text()='详情']")
        self.click('x', "//div[text()=' 受理计划 ']")
        self.logger.info('箱综合查询：换箱出场箱，计划箱状态为C')
        table = Gtos_table(self.driver, 13)
        check.equal(table.get_value('计划箱状态'), 'C')
