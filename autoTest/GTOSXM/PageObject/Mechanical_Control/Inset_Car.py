from Base.basepage import BasePage
from GTOSXM.Config import config
from GTOSXM.Controls.Gtos_table import Gtos_table


class Inset_Car(BasePage):
    """
    查看可用集卡
    """

    def choice_job(self, name):
        """
        选择作业路
        """
        self.logger.info('内集卡控制-查看可用内集卡号')
        textable = Gtos_table(self.driver, 3)
        textable.left_select(name)

    def choice_cars(self, job, value):
        """
        选择等待装货集卡号
        """

        textable = Gtos_table(self.driver, 2)
        self.left_click('x', "//span[text()='作业步骤']")
        self.left_clickandsend('x',
                               "(//div[@class='ag-header-container'])[2]//input[@aria-label='危品资质 Filter Input']",
                               '无资质')
        config.carnumber = textable.select_row(f'{job}', f'{value}')
        self.logger.info("集卡号:"+config.carnumber)
