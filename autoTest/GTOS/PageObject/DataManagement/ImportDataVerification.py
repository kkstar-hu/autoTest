from selenium.webdriver import ActionChains
from Base.basepage import BasePage
from GTOS.Controls.text import Gtos_text
from GTOS.Config import config
from GTOS.Controls.Gtos_table import Gtos_table


class Import_data_verification(BasePage):
    """
    进口资料校验
    """

    def retrieval(self):
        """
        检索
        """
        Gtextinput = Gtos_text(self.driver)
        Gtextinput.search_select_by_label('船名航次', config.importNumber)
        self.click('x', "//span[text()='检索']")

    def verification(self, position):
        """
        校验
        """
        Gtable = Gtos_table(self.driver)
        Gtable.left_click('x', "//span[text()='船箱位校验']")
        e1 = self.get_element('x',
                              "((//div[@class ='ag-center-cols-clipper'])[3]//div[@class='ag-cell "
                              "ag-cell-not-inline-editing ag-cell-normal-height ag-cell-value'])[8]")
        ActionChains(self.driver).click(e1).send_keys(f'{position}').perform()
        self.left_click('x', "//span[text()='保存']")
        self.check_alert('修改成功')
        self.close_alert('修改成功')
