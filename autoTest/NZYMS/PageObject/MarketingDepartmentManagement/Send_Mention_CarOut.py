import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from Base.basepage import BasePage
from Commons.Controls.table import Table
from Commons.Controls.text import text


class Send_Mention_CarOut(BasePage):
    """
    送提货车辆放行确认
    """
    def input_carnumber(self,input):
        """
        输入车牌号
        """
        self.logger.info('车辆放行：输入车牌号')
        textInput = text(self.driver)
        textInput.input_by_placeholder('请输入车号',input['车牌']+input['车号'])

    def retrieve(self):
        """
        点击检索按钮
        """
        self.click('xpath', "//span[text()='检索']")

    def reset(self):
        """
        点击重置按钮
        """
        self.click('xpath', "//span[text()='重置']")

    def car_release(self):
        """
        确认放行按钮
        """
        self.click('xpath',"//span[text()='确认放行']")


    def process(self,input):
        """
        送提货车辆放行流程
        """
        self.input_carnumber(input)
        self.retrieve()
        self.logger.info('车辆放行：勾选')
        table= Table(self.driver)
        table.tick_off_box(1)
        self.logger.info('步骤3：放行按钮点击')
        self.element_wait_disappear(By.XPATH, "//div[@role='alert']//p")
        self.car_release()
        self.click("xpath", "//div[@class='el-message-box__btns']//span[contains(text(),'确定')]")
        self.check_alert("放行成功")

