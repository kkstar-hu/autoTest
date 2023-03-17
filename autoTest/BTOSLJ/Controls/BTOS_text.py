# -*- coding:utf-8 -*-
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import NoSuchElementException
from selenium.webdriver import Keys
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.wait import WebDriverWait

from Base.basepage import BasePage

class BtosText(BasePage):
    '''
        drawer:抽屉
        dialog:弹窗
    '''
    def input_text_by_label_drawer(self, label : str, value : str):
        try:
            # 由于前端基础组件的错误，诞生了这段不可名状的xpath
            e1 = self.get_element_wait("xpath", f"(//div[@class='dialogCon']//label[text()='{label}']/following-sibling::div/div[1]//input[not(@tabindex)])[1]")
        except NoSuchElementException:
            self.logger.info("定位不到元素")
        else:
            e1.click()
            e1.send_keys(value)

    def input_by_for_drawer(self, f : str, value : str):
        try:
            e1 = self.get_element_wait("xpath", f"(//div[@class='dialogCon']//label[@for='{f}']/following-sibling::div/div[1]//input[not(@tabindex)])[1]")
        except NoSuchElementException:
            self.logger.info("定位不到元素")
        else:
            e1.click()
            e1.send_keys(value)

    def select_by_label_drawer(self, label : str, value : str, t = 0):
        try:
            e1 = self.get_element_wait("xpath", f"(//div[@class='dialogCon']//label[text()='{label}']/following-sibling::div/div[1]//input[not(@tabindex)])[1]")
            e1.click()
            e1.send_keys(value)
            path = f"//div[starts-with(@class,'el-select-dropdown el-popper') and not (contains(@style,'display: none'))]//span[text()='{value}']/.."
            self.wait_visible((By.XPATH,path))
        except Exception as e:
            self.logger.error("定位不到元素:", e)
        else:
            if(t):   # 针对模糊搜索调接口的下拉框，需要等待
                time.sleep(t)
            self.click("xpath", path)

    def select_by_label_index(self, label : str, index : int):
        try:
            e1 = self.get_element_wait("xpath", f"(//div[@class='dialogCon']//label[text()='{label}']/following-sibling::div/div[1]//input[not(@tabindex)])[1]")
            e1.click()
        except Exception as e:
            self.logger.error("定位不到元素:", e)
        else:
            self.click("xpath", f"//div[starts-with(@class,'el-select-dropdown el-popper') and not(contains(@style,'display: none'))]//li[{index+1}]")


    def input_time_by_label_drawer(self, label : str, time : str):
        try:
            e1 = self.get_element_wait("xpath", f"(//div[@class='dialogCon']//label[text()='{label}']/following-sibling::div/div[1]//input[not(@tabindex)])[1]")
        except Exception as e:
            self.logger.error("定位不到元素:", e)
        else:
            e1.click()
            e1.send_keys(time, Keys.ENTER)

    # 货名       vue的独立组件
    def mul_select_by_label_drawer(self, label : str, value : str):
        try:
            e1 = self.get_element("xpath", f"//div[@class='dialogCon']//input[@class='vue-treeselect__input']")
            e1.click()
            for x in value.split(","):
                e1.send_keys(x, Keys.ENTER)
        except NoSuchElementException as e:
            self.logger.error("定位不到元素:", e)
        else:
            # self.click("xpath", "//div[@class='vue-treeselect__control-arrow-container']")
            pass

    # 多选框，按索引选择一个
    def mul2_select_by_label_index(self, label : str, index : int):
        try:
            e1 = self.get_element_wait("xpath", f"(//div[@class='dialogCon']//label[text()='{label}']/following-sibling::div/div[1]//input[not(@tabindex)])[1]")
            e1.click()
        except NoSuchElementException as e:
            self.logger.error("定位不到元素:", e)
        else:
            self.click("xpath", f"//div[starts-with(@class,'el-select-dropdown el-popper') and not(contains(@style,'display: none'))]//li[{index+1}]")
            self.click("xpath", f"//div[@class='dialogCon']//label[text()='{label}']")

    def wait_visible(self, locator : set, ses = 5):
        try:
            WebDriverWait(self.driver, 5, 1).until(EC.visibility_of_element_located(locator))
        except Exception as e:
            self.logger.error("等待元素可见失败:", e)

    def wait_clickable(self, locator : set, ses = 5):
        try:
            WebDriverWait(self.driver, 5, 1).until(EC.element_to_be_clickable(locator))
        except Exception as e:
            self.logger.error("等待元素可点击失败:", e)

    # 如果前端正确，应该使用这个进行下拉选择
    def select_by_label(self, label : str, value : str, t = 0):
        try:
            e1 = self.get_element_wait("xpath", f"//label[contains(text(),'{label}')]/following-sibling::div//input")
            e1.click()
            e1.send_keys(value)
            path = f"//div[starts-with(@class,'el-select-dropdown el-popper') and not (contains(@style,'display: none'))]//span[text()='{value}']/.."
            self.wait_visible((By.XPATH,path))
        except Exception as e:
            self.logger.error("定位不到元素:", e)
        else:
            if(t):   # 针对模糊搜索调接口的下拉框，需要等待
                time.sleep(t)
            self.click("xpath", path)


