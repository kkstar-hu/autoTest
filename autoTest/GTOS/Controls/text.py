from selenium.common import NoSuchElementException
from selenium.webdriver import ActionChains

from Base.basepage import BasePage
from Commons.Controls.text import text


class Gtos_text(BasePage):
    #label:输入标签名，value：输入值

    def search_input_by_label(self,label,value):
        try:
            self.input("xpath",f"//form[@class='el-form common-search__form']//label[contains(text(),'{label}')]//following-sibling::div//input",value)
        except NoSuchElementException:
            raise Exception("定位不到元素")

    def search_select_by_label(self, label, value):
        try:
            self.input_no_clear("xpath",f"//label[contains(text(),'{label}')]//following-sibling::div//input",value)
            self.click("xpath",
                       f"//div[starts-with(@class,'el-select-dropdown el-popper') and not (contains(@style,'display: none'))]//span[contains(text(),'{value}')]")
        except NoSuchElementException:
            raise Exception("定位不到元素")

    def search_input_by_number(self, label, value,index=1):
        try:
            self.input_by_index("xpath",f"//form[@class='el-form common-search__form']//label[contains(text(),'{label}')]//following-sibling::div//input",value,index)
        except NoSuchElementException:
            raise Exception("定位不到元素")


    def input_noclear_placeholder_click(self, name, value,index = 1):
        try:
            self.input_no_clear("xpath", f"(//input[@placeholder='{name}'])[{index}]", value)
            self.click("xpath", f"//span[text()='{value}']")
        except NoSuchElementException:
            raise Exception("定位不到元素")


    #无type元素操作
    def no_elements_click(self,name,index=1):
        em = self.get_element('xpath',f"(//span[text()='{name}'])[{index}]")
        ActionChains(self.driver).move_to_element(em).click().perform()

    def input_by_label(self,label,value):
        try:
            self.input("xpath",f"//label[contains(text(),'{label}')]//following-sibling::div//input",value)
        except NoSuchElementException:
            raise Exception("定位不到元素")

    #精确查找label
    def input_by_label_exact(self,label,value):
        try:
            self.input("xpath",f"//label[text()='{label}']//following-sibling::div//input",value)
        except NoSuchElementException:
            raise Exception("定位不到元素")


    #name:输入单行文本款的显示信息
    def input_by_placeholder(self, name, value):
        try:
            self.input("xpath",f"//input[@placeholder='{name}']",value)
        except NoSuchElementException:
            raise Exception("定位不到元素")

    def input_by_number(self, label, value,index=1):
        try:
            self.input_by_index("xpath",f"//label[contains(text(),'{label}')]//following-sibling::div//input",value,index)
        except NoSuchElementException:
            raise Exception("定位不到元素")

    #获取单行文本的值
    def get_text_value(self,label,index=1):
        return self.get_text_index("xpath",f"//label[contains(text(),'{label}')]//following-sibling::div//input",index)

    def text_isenable(self,label,index=0):
        return self.get_enable("xpath",f"//label[contains(text(),'{label}')]//following-sibling::div//input",index)

    def select_by_label(self, label, value):
        try:
            self.click("xpath",f"//label[contains(text(),'{label}')]//following-sibling::div//input")
            self.click("xpath",f"//div[starts-with(@class,'el-select-dropdown el-popper') and not (contains(@style,'display: none'))]//span[text()='{value}']")
        except NoSuchElementException:
            raise Exception("定位不到元素")

    def select_by_label_exact(self, label, value):
        try:
            self.click("xpath",f"//label[text()='{label}']//following-sibling::div//input")
            self.click("xpath",f"//div[starts-with(@class,'el-select-dropdown el-popper') and not (contains(@style,'display: none'))]//span[text()='{value}']")
        except NoSuchElementException:
            raise Exception("定位不到元素")

    def select_by_placeholder(self, name, value):
        try:
            self.click("xpath",f"//input[@placeholder='{name}']")
            self.click("xpath", f"//div[starts-with(@class,'el-select-dropdown el-popper') and not (contains(@style,'display: none'))]//span[text()='{value}']")
        except NoSuchElementException:
            raise Exception("定位不到元素")

    def select_by_placeholder_index(self,name,value,index=1):
        try:
            self.get_elements('xpath', f'//input[@placeholder="{name}"]')[index].click()
            self.click("xpath", f"//div[starts-with(@class,'el-select-dropdown el-popper') and not (contains(@style,'display: none'))]//span[text()='{value}']")
        except NoSuchElementException:
            raise Exception("定位不到元素")
        #新

    def select_by_index(self, label, value,index=1):
        try:
            self.click_by_index("xpath", f"//label[contains(text(),'{label}')]//following-sibling::div//input",index)
            self.click("xpath", f"//div[starts-with(@class,'el-select-dropdown el-popper') and not (contains(@style,'display: none'))]//span[text()='{value}']")
        except NoSuchElementException:
            raise Exception("定位不到元素")


    def select_clickOption(self, value):
        try:
            self.click("xpath", f"//div[starts-with(@class,'el-select-dropdown el-popper') and not (contains(@style,'display: none'))]//span[text()='{value}']")
        except NoSuchElementException:
            raise Exception("定位不到元素")


    #多行文本输入
    def textarea_by_label(self, label, value):
        try:
            self.input("xpath",
                       f"//label[contains(text(),'{label}')]//following-sibling::div//textarea",value)
        except NoSuchElementException:
            raise Exception("定位不到元素")
