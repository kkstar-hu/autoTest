from selenium.common import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from Base.basepage import BasePage
from selenium.webdriver.common.keys import Keys
import time
from Commons.Controls.text import text

class Out_Confirm(BasePage):
    """
    道口管理-----出场确认
    """

    def out_confirm(self,input):
        """选择道口，堆场"""
        self.logger.info('步骤1：选择道口（进场专用/01）')
        textInput = text(self.driver)
        self.waitloading()
        if input['堆场'] is not None:
            textInput.select_by_label("堆场", input["堆场"])
        if input['道口'] is not None:
            textInput.select_by_label("道口", input['道口'])


    def choice_car(self,input):
        """选择出场车辆"""
        try:
            self.logger.info('步骤2:选择对应车辆，确认出场')
            self.get_element('xpath',f"//span[text()='{input['车牌'] + input['车号']}']").click()
        except NoSuchElementException:
            raise Exception("定位不到元素")
        self.waitloading()


    def confirm_button(self):
        """
        出场确认按钮
        """
        self.logger.info('步骤3：确认出场')
        self.element_wait_disappear(By.XPATH, "//div[@role='alert']//p")
        # WebDriverWait(self.driver, 5, 1).until_not(
        #     EC.presence_of_element_located((By.XPATH, "//div[@role='alert']//p")))
        self.get_element('xpath', "//span[text()='确认出场']").click()
        self.check_alert("成功")
