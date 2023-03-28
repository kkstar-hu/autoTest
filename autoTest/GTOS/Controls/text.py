from selenium.common import NoSuchElementException
from selenium.webdriver import ActionChains
from Base.basepage import BasePage


class Gtos_text(BasePage):
    def search_select_by_label(self, label, value):
        """
        控件：单行文本，先输入后点击下拉框值，在查询条件中用的多
        label:输入标签名，value：输入值
        """
        try:
            self.input_no_clear("xpath",f"//label[contains(text(),'{label}')]//following-sibling::div//input",value)
            self.click("xpath",
                       f"//div[starts-with(@class,'el-select-dropdown el-popper') and not (contains(@style,'display: none'))]//span[contains(text(),'{value}')]")
        except NoSuchElementException:
            self.logger.error(f"定位不到下拉控件标签名:{label}")
            raise Exception("定位不到元素")

    def input_noclear_placeholder_click(self, name, value,index = 1):
        """
        控件：单行文本，先输入后点击下拉框值，在查询条件中用的多
        name:输入属性placeholder，value：输入值
        """
        try:
            self.input_no_clear("xpath", f"(//input[@placeholder='{name}'])[{index}]", value)
            self.click("xpath",
                       f"//div[starts-with(@class,'el-select-dropdown el-popper') and not (contains(@style,'display: none'))]//span[contains(text(),'{value}')]")
        except NoSuchElementException:
            self.logger.error(f"定位不到控件placeholder:{name}")
            raise Exception("定位不到元素")

    #无type元素操作
    def no_elements_click(self,name,index=1):
        em = self.get_element('xpath',f"(//span[text()='{name}'])[{index}]")
        ActionChains(self.driver).move_to_element(em).click().perform()

    def input_by_label(self,label,value):
        """
        控件：单行文本
        label:输入标签名，value：输入值
        """
        try:
            self.input("xpath",f"//label[contains(text(),'{label}')]//following-sibling::div//input",value)
        except NoSuchElementException:
            self.logger.error(f"定位不到单行文本控件标签名:{label}")
            raise Exception("定位不到元素")

    def input_by_placeholder(self, name, value):
        """
        控件：单行文本
        name:输入属性placeholder，value：输入值
        """
        try:
            self.input("xpath",f"//input[@placeholder='{name}']",value)
        except NoSuchElementException:
            self.logger.error(f"定位不到单行文本控件placeholder:{name}")
            raise Exception("定位不到元素")

    def input_by_number(self, label, value,index=1):
        """
        控件：单行文本
        label:输入标签名，value：输入值，index：当页面存在多个相同的控件，通过index区分
        """
        try:
            self.input_by_index("xpath",f"//label[contains(text(),'{label}')]//following-sibling::div//input",value,index)
        except NoSuchElementException:
            self.logger.error(f"定位不到单行文本控件标签名:{label}")
            raise Exception("定位不到元素")

    #获取单行文本的值
    def get_text_value(self,label,index=1):
        try:
            return self.get_text_index("xpath",f"//label[contains(text(),'{label}')]//following-sibling::div//input",index)
        except NoSuchElementException:
            self.logger.error(f"获取值定位不到标签名:{label}")
            raise Exception("定位不到元素")

    # 判断控件是否可编辑
    def text_isenable(self,label,index=0):
        return self.get_enable("xpath",f"//label[contains(text(),'{label}')]//following-sibling::div//input",index)

    def select_by_label(self, label, value):
        """
        控件：下拉框
        label:输入标签名，value：输入值
        """
        try:
            self.click("xpath",f"//label[contains(text(),'{label}')]//following-sibling::div//input")
            self.click("xpath",f"//div[starts-with(@class,'el-select-dropdown el-popper') and not (contains(@style,'display: none'))]//span[text()='{value}']")
        except NoSuchElementException:
            self.logger.error(f"定位不到下拉控件标签名:{label}")
            raise Exception("定位不到元素")

    def multi_select_by_label(self, label, value):
        """
        控件：多选下拉框
        label:输入标签名，value：输入值
        """
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
            self.click("xpath",f"//label[text()='{label}']//following-sibling::div//input")
            self.click("xpath",f"//div[starts-with(@class,'el-select-dropdown el-popper') and not (contains(@style,'display: none'))]//span[text()='{value}']")
        except NoSuchElementException:
            self.logger.error(f"定位不到下拉控件标签名:{label}")
            raise Exception("定位不到元素")

    def select_by_placeholder(self, name, value):
        """
        控件：下拉框
        name:placeholder属性, value：输入值
        """
        try:
            self.click("xpath",f"//input[@placeholder='{name}']")
            self.click("xpath", f"//div[starts-with(@class,'el-select-dropdown el-popper') and not (contains(@style,'display: none'))]//span[text()='{value}']")
        except NoSuchElementException:
            self.logger.error(f"定位不到下拉框控件placeholder:{name}")
            raise Exception("定位不到元素")

    def select_by_placeholder_index(self,name,value,index=1):
        """
        控件：下拉框
        name:placeholder属性, value：输入值, index：当页面存在多个相同的控件，通过index区分
        """
        try:
            self.get_elements('xpath', f'//input[@placeholder="{name}"]')[index].click()
            self.click("xpath", f"//div[starts-with(@class,'el-select-dropdown el-popper') and not (contains(@style,'display: none'))]//span[text()='{value}']")
        except NoSuchElementException:
            self.logger.error(f"定位不到下拉框控件placeholder:{name}")
            raise Exception("定位不到元素")

    def select_by_index(self, label, value,index=1):
        """
        控件：下拉框
        label:输入标签名，value：输入值, index：当页面存在多个相同的控件，通过index区分
        """
        try:
            self.click_by_index("xpath", f"//label[contains(text(),'{label}')]//following-sibling::div//input",index)
            self.click("xpath", f"//div[starts-with(@class,'el-select-dropdown el-popper') and not (contains(@style,'display: none'))]//span[text()='{value}']")
        except NoSuchElementException:
            self.logger.error(f"定位不到下拉框控件标签名:{label}")
            raise Exception("定位不到元素")

    # 点击下拉框值
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
                       f"//label[contains(text(),'{label}')]//following-sibling::div//textarea",value)
        except NoSuchElementException:
            self.logger.error(f"定位不到多行文本:{label}")
            raise Exception("定位不到元素")
