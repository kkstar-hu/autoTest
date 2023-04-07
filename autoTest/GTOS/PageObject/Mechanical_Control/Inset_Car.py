from Base.basepage import BasePage
from GTOS.Config import config
from GTOS.Controls.Gtos_table import Gtos_table


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

    def choice_car(self):
        """
        选择可用集卡号
        """
        list1 = []
        row = []
        value = self.get_element('x', "(//div[@class='ag-center-cols-container'])[2]")
        value_text = list(value.get_attribute('textContent').split('Q002'))
        del value_text[0]
        for i in value_text:
            if '等待装车' in i:
                row.append(value_text.index(i))
        car_value = self.get_element('x', "(//div[@class='ag-pinned-left-cols-container'])[2]")
        car_text = car_value.get_attribute('textContent').replace(' ', '').split('\n')
        for i in car_text:
            if len(i) >= 2:
                list1.append(i[0:4])
        config.carnumber = list1[row[1]]

    def choice_cars(self, job, value):
        """
        选择等待装货集卡号
        """
        textable = Gtos_table(self.driver, 2)
        self.left_click('x', "//span[text()='作业步骤']")
        config.carnumber = textable.select_row(f'{job}', f'{value}')
