import random
import pytest_check as check
from Base.basepage import BasePage
from GTOSXM.Controls.text import Gtos_text
from GTOSXM.Config import configinterface
from GTOSXM.Controls.Gtos_table import Gtos_table


class Incoming_job_list(BasePage):
    """
    进场作业列表
    """

    def input_values(self, boxnumber):
        """
        输入查询内容
        """
        self.logger.info('进场作业列表：输入数据')
        textInput = Gtos_text(self.driver)
        textInput.input_by_label("箱号", boxnumber)

    def check_first(self):
        """
        第一次查验
        """
        self.logger.info('进场作业列表：查验作业-允许作业状态')
        self.click('xpath', "//span[text()='检索']")
        tablecheck = Gtos_table(self.driver)
        check.equal(tablecheck.get_value('作业状态'), '允许作业')

    def check_second(self):
        """
        第二次查验
        """
        self.logger.info('进场作业列表：查验作业-完成状态')
        self.click('xpath', "//span[text()='检索']")
        tablecheck = Gtos_table(self.driver)
        check.equal(tablecheck.get_value('作业状态'), '完成')

    def refund_box(self):
        """
        退换箱
        """
        self.logger.info('进场作业列表：退箱操作')
        self.click('x', "//span[text()='退箱']")
        textInput = Gtos_text(self.driver)
        textInput.select_by_label_time("取消原因", '自然因素')
        self.click('c', "el-checkbox__inner")
        self.click('x', "//label[text()='换箱']//following-sibling::div//input")
        configinterface.boxNumbertwo = self.give_list()
        self.logger.info(f'换箱箱号：{configinterface.boxNumbertwo}')
        self.click('x', f"//li//span[text()='{configinterface.boxNumbertwo}']")
        self.click('x', "//span[text()='保 存']")
        self.check_alert('退箱成功')
        self.close_alert('退箱成功')

    def give_list(self):
        """
        获取可用箱号列表,并随机获取一个可用的箱号
        """
        boxid = []
        a = self.get_elements("xpath", "(//div[@class='el-scrollbar'])[5]//li")
        # 获取当前可使用的所有箱号，并加入列表
        for i in a:
            boxid.append(i.get_attribute('innerText'))
        b = random.choice(boxid)  # 随机选择其中一个箱号

        return b