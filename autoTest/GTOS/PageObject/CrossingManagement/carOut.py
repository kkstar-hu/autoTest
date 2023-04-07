import time
from Base.basepage import BasePage
from GTOS.Controls.text import Gtos_text


class Car_Out(BasePage):
    """
    车辆出场
    """

    def input_values(self, input, boxnumber):
        """
        输入车辆，箱号
        """
        self.logger.info('车辆出场操作')
        textInput = Gtos_text(self.driver)
        textInput.select_by_label("集卡号", input["车牌"])
        self.get_element('xpath', "//input[@placeholder='请输入集卡号']").send_keys(input["集卡编号"])
        self.get_element('xpath', "//input[@placeholder='请输入箱号']").send_keys(boxnumber)
        self.click('xpath', "(//div[@class='el-select el-select--small nzctos-select-wrap'])[2]")
        self.click('xpath', "//li//span[text()='B06']")

    def retrieve(self):
        """
        检索
        """
        self.click('xpath', "//span[text()='检索']")
        time.sleep(1)

    def confirm_out_picking(self):
        """
        确认出场——提箱流程
        """
        self.click('xpath', "//span[text()='确认出场']")
        self.click('xpath', "//span[contains(text(),'否')]")
        self.check_alert('车辆出场成功')

    def confirm_out_loadingAndLifting(self):
        """
        确认出场-直装流程
        """
        self.click('xpath', "//span[text()='确认出场']")
        self.check_alert('车辆出场成功')
