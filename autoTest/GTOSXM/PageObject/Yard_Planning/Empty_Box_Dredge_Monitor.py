from Base.basepage import BasePage
from GTOSXM.Controls.Gtos_table import Gtos_table


class Empty_Box_Dredge_Monitor(BasePage):
    """
    空箱疏运监控
    """

    def monitor_switch(self):
        """
        监控启用、停用
        """
        self.logger.info('监控：查看监控状态')
        self.left_clickandsend('x', "//input[@aria-label='箱区 Filter Input']", 'Q9')
        self.left_click('x',"(//div[@class='nzctos-grid__selection_buttons']//span[text()='全'])[1]")
        Gtable = Gtos_table(self.driver)
        self.logger.info('监控：操作启用')
        self.click('x', "(//span[text()='启用'])[1]")
        self.check_alert('启用成功')
        self.close_alert('启用成功')


