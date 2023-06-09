# -*- coding:utf-8 -*-
import time

from DrissionPage.action_chains import ActionChains
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
    def input_text_by_label_drawer(self, label: str, value: str):
        try:
            # 由于前端基础组件的错误，诞生了这段不可名状的xpath
            self.wait_clickable((By.XPATH, f"(//div[@class='dialogCon']//label[text()='{label}']/following-sibling::div/div[1]//input[not(@tabindex)])[1]"))
            e1 = self.get_element("xpath", f"(//div[@class='dialogCon']//label[text()='{label}']/following-sibling::div/div[1]//input[not(@tabindex)])[1]")
        except Exception:
            self.logger.error(f"定位元素失败:", exc_info=True)
        else:
            e1.click()
            e1.send_keys(value)

    def input_by_for_drawer(self, f: str, value: str):
        try:
            e1 = self.get_elements_wait("xpath", f"(//div[@class='dialogCon']//label[@for='{f}']/following-sibling::div/div[1]//input[not(@tabindex)])[1]")
        except Exception:
            self.logger.error(f"定位元素失败:", exc_info=True)
        else:
            e1.click()
            e1.send_keys(value)

    def select_by_label_drawer(self, label : str, value : str, t = 0):
        try:
            e1 = self.get_elements_wait("xpath", f"(//div[@class='dialogCon']//label[text()='{label}']/following-sibling::div/div[1]//input[not(@tabindex)])[1]")
            e1.click()
            e1.send_keys(value)
            path = f"//div[starts-with(@class,'el-select-dropdown el-popper') and not (contains(@style,'display: none'))]//span[text()='{value}']/.."
            self.wait_visible((By.XPATH, path))
        except Exception:
            self.logger.error(f"定位元素失败:", exc_info=True)
        else:
            if(t):   # 针对模糊搜索调接口的下拉框，需要等待
                time.sleep(t)
            self.click("xpath", path)

    def select_by_label_index(self, label: str, index: int):
        try:
            e1 = self.get_elements_wait("xpath", f"(//div[@class='dialogCon']//label[text()='{label}']/following-sibling::div/div[1]//input[not(@tabindex)])[1]")
            e1.click()
        except Exception:
            self.logger.error(f"定位元素失败:", exc_info=True)
        else:
            self.click("xpath", f"//div[starts-with(@class,'el-select-dropdown el-popper') and not(contains(@style,'display: none'))]//li[{index+1}]")

    def input_time_by_label_drawer(self, label: str, time: str):
        try:
            e1 = self.get_elements_wait("xpath", f"(//div[@class='dialogCon']//label[text()='{label}']/following-sibling::div/div[1]//input[not(@tabindex)])[1]")
        except Exception:
            self.logger.error(f"定位元素失败:", exc_info=True)
        else:
            e1.click()
            e1.send_keys(time, Keys.ENTER)

    # 货名       vue的独立组件
    def mul_select_by_label_drawer(self, label: str, value: str):
        try:
            e1 = self.get_element("xpath", f"//div[@class='dialogCon']//input[@class='vue-treeselect__input']")
            e1.click()
            for x in value.split(","):
                e1.send_keys(x, Keys.ENTER)
        except Exception:
            self.logger.error(f"定位元素失败:", exc_info=True)
        else:
            # self.click("xpath", "//div[@class='vue-treeselect__control-arrow-container']")
            pass

    # 多选框，按索引选择一个
    def mul2_select_by_label_index(self, label: str, index: int):
        try:
            e1 = self.get_elements_wait("xpath", f"(//div[@class='dialogCon']//label[text()='{label}']/following-sibling::div/div[1]//input[not(@tabindex)])[1]")
            e1.click()
            self.wait_clickable((By.XPATH, f"//div[starts-with(@class,'el-select-dropdown el-popper') and not(contains(@style,'display: none'))]//li[{index+1}]"))
            self.click("xpath", f"//div[starts-with(@class,'el-select-dropdown el-popper') and not(contains(@style,'display: none'))]//li[{index+1}]")
        except Exception:
            self.logger.error(f"定位元素失败:", exc_info=True)
        else:
            self.click("xpath", f"//div[@class='dialogCon']//label[text()='{label}']")

    def wait_visible(self, locator: set, ses=5):
        try:
            WebDriverWait(self.driver, 5, 1).until(EC.visibility_of_element_located(locator))
        except Exception:
            self.logger.error(f"等待元素可见失败:", exc_info=True)

    def wait_clickable(self, locator : set, ses=5):
        try:
            WebDriverWait(self.driver, 5, 1).until(EC.element_to_be_clickable(locator))
        except Exception:
            self.logger.error(f"等待元素可点击失败:", exc_info=True)

    # 如果前端正确，应该使用这个进行下拉选择
    def select_by_label_correct(self, label: str, value: str, t=0):
        try:
            e1 = self.get_elements_wait("xpath", f"//label[contains(text(),'{label}')]/following-sibling::div//input")
            e1.click()
            e1.send_keys(value)
            path = f"//div[starts-with(@class,'el-select-dropdown el-popper') and not (contains(@style,'display: none'))]//span[text()='{value}']/.."
            self.wait_visible((By.XPATH, path))
        except Exception:
            self.logger.error(f"定位元素失败:", exc_info=True)
        else:
            if(t):   # 针对模糊搜索调接口的下拉框，需要等待
                time.sleep(t)
            self.click("xpath", path)

    def select_by_label_ship(self, label, value):
        """
        船名航次特殊控件选择
        """
        try:
            self.click("xpath", f"//label[text()='{label}']//following-sibling::div//input")
            time.sleep(0.5)
            self.click("xpath",
                       f"//div[starts-with(@class,'el-select-dropdown el-popper') and not (contains(@style,'display: none'))]"
                       f"//li[starts-with(@class,'el-select-dropdown__item')]/div[contains(text(),'{value}')]")
        except NoSuchElementException:
            self.logger.error(f"定位不到下拉控件标签名:{label}")
            raise Exception("定位不到元素")

    def search_select_by_label(self, label, value):
        try:
            self.input_no_clear("xpath", f"//label[contains(text(),'{label}')]//following-sibling::div//div[not (@ style='display: none;')] // input[not (@ disabled)]",value)
            self.click("xpath",
                       f"//div[starts-with(@class,'el-select-dropdown el-popper') and not (contains(@style,'display: none'))]//span[contains(text(),'{value}')]")
        except NoSuchElementException:
            self.logger.error(f"定位不到下拉控件标签名:{label}")
            raise Exception("定位不到元素")

    def input_noclear_placeholder_click(self, name, value, index=1):
        try:
            self.input_no_clear("xpath", f"(//input[@placeholder='{name}'])[{index}]", value)
            self.click("xpath",
                       f"//div[starts-with(@class,'el-select-dropdown el-popper') and not (contains(@style,'display: none'))]//span[contains(text(),'{value}')]")
        except NoSuchElementException:
            self.logger.error(f"定位不到控件placeholder:{name}")
            raise Exception("定位不到元素")

    #无type元素操作
    def no_elements_click(self, name, index=1):
        em = self.get_element('xpath', f"(//span[text()='{name}'])[{index}]")
        ActionChains(self.driver).move_to_element(em).click().perform()

    def input_by_label(self, label, value):
        try:
            self.input("xpath", f"//label[contains(text(),'{label}')]//following-sibling::div//div[not (@ style='display: none;')] // input[not (@ disabled)]",value)
        except NoSuchElementException:
            self.logger.error(f"定位不到单行文本控件标签名:{label}")
            raise Exception("定位不到元素")

    # name:输入单行文本款的显示信息
    def input_by_placeholder(self, name, value):
        try:
            self.input("xpath", f"//input[@placeholder='{name}']", value)
        except NoSuchElementException:
            self.logger.error(f"定位不到单行文本控件placeholder:{name}")
            raise Exception("定位不到元素")

    def input_by_number(self, label, value, index=1):
        """
        页面多个控件，传入index,从0开始
        """
        try:
            self.input_by_index("xpath", f"//label[contains(text(),'{label}')]//following-sibling::div//div[not (@ style='display: none;')] // input[not (@ disabled)]", value, index)
        except NoSuchElementException:
            self.logger.error(f"定位不到单行文本控件标签名:{label}")
            raise Exception("定位不到元素")

    def text_isenable(self, label, index=0):
        return self.get_enable("xpath", f"//label[contains(text(),'{label}')]//following-sibling::div//input", index)

    def select_by_label(self, label, value):
        try:
            self.click("xpath", f"//label[contains(text(),'{label}')]//following-sibling::div//div[not (@ style='display: none;')] // input[not (@ disabled)]")
            self.click("xpath", f"//div[starts-with(@class,'el-select-dropdown el-popper') and not (contains(@style,'display: none'))]//span[text()='{value}']")
        except NoSuchElementException:
            self.logger.error(f"定位不到下拉控件标签名:{label}")
            raise Exception("定位不到元素")

    def select_by_label_time(self, label, value):
        try:
            self.click("xpath", f"//label[contains(text(),'{label}')]//following-sibling::div//div[not (@ style='display: none;')] // input[not (@ disabled)]")
            time.sleep(0.5)
            self.click("xpath", f"//div[starts-with(@class,'el-select-dropdown el-popper') and not (contains(@style,'display: none'))]//span[text()='{value}']")
        except NoSuchElementException:
            self.logger.error(f"定位不到下拉控件标签名:{label}")
            raise Exception("定位不到元素")

    def multi_select_by_label(self, label, value):
        try:
            self.click("xpath", f"//label[contains(text(),'{label}')]//following-sibling::div//input")
            for x in value.split(","):
                self.click("xpath",
                           f"//div[starts-with(@class,'el-select-dropdown el-popper') and not (contains(@style,'display: none'))]//span[text()='{x}']")
        except NoSuchElementException:
            self.logger.error(f"定位不到多选下拉控件标签名:{label}")
            raise Exception("定位不到元素")

    def select_by_label_exact(self, label, value):
        try:
            self.click("xpath",f"//label[text()='{label}']//following-sibling::div//div[not (@ style='display: none;')] // input[not (@ disabled)]")
            self.click("xpath",f"//div[starts-with(@class,'el-select-dropdown el-popper') and not (contains(@style,'display: none'))]//span[text()='{value}']")
        except NoSuchElementException:
            self.logger.error(f"定位不到下拉控件标签名:{label}")
            raise Exception("定位不到元素")

    def select_by_placeholder(self, name, value):
        try:
            self.click("xpath",f"//input[@placeholder='{name}']")
            self.click("xpath", f"//div[starts-with(@class,'el-select-dropdown el-popper') and not (contains(@style,'display: none'))]//span[text()='{value}']")
        except NoSuchElementException:
            self.logger.error(f"定位不到下拉框控件placeholder:{name}")
            raise Exception("定位不到元素")

    def select_by_placeholder_index(self, name, value, index=1):
        try:
            self.get_elements('xpath', f'//input[@placeholder="{name}"]')[index].click()
            self.click("xpath", f"//div[starts-with(@class,'el-select-dropdown el-popper') and not (contains(@style,'display: none'))]//span[text()='{value}']")
        except NoSuchElementException:
            self.logger.error(f"定位不到下拉框控件placeholder:{name}")
            raise Exception("定位不到元素")
        #新

    def select_by_index(self, label, value, index=1):
        try:
            self.click_by_index("xpath", f"//label[contains(text(),'{label}')]//following-sibling::div//div[not (@ style='display: none;')] // input[not (@ disabled)]", index)
            time.sleep(0.5)
            self.click("xpath", f"//div[starts-with(@class,'el-select-dropdown el-popper') and not (contains(@style,'display: none'))]//span[text()='{value}']")
        except NoSuchElementException:
            self.logger.error(f"定位不到下拉框控件标签名:{label}")
            raise Exception("定位不到元素")

    def select_clickOption(self, value):
        try:
            self.click("xpath", f"//div[starts-with(@class,'el-select-dropdown el-popper') and not (contains(@style,'display: none'))]//span[text()='{value}']")
        except NoSuchElementException:
            self.logger.error(f"定位不到下拉框控件值:{value}")
            raise Exception("定位不到元素")

    #多行文本输入
    def textarea_by_label(self, label, value):
        try:
            self.input("xpath",
                       f"//label[contains(text(),'{label}')]//following-sibling::div//textarea", value)
        except NoSuchElementException:
            self.logger.error(f"定位不到多行文本:{label}")
            raise Exception("定位不到元素")


