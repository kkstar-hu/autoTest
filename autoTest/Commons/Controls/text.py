from selenium.common import NoSuchElementException

from Base.basepage import BasePage



class text(BasePage):
    #label:输入标签名，value：输入值

    def input_by_label(self,label,value):
        try:
            self.input("xpath",f"//form[@class='el-form']//label[contains(text(),'{label}')]//following-sibling::div//input",value)
        except NoSuchElementException:
            self.logger.error(f"定位不到单行文本控件标签名:{label}")
            raise Exception("定位不到元素")

    #name:输入单行文本款的显示信息
    def input_by_placeholder(self, name, value):
        try:
            self.input("xpath",f"//input[@placeholder='{name}']",value)
        except NoSuchElementException:
            self.logger.error(f"定位不到单行文本控件placeholder:{name}")
            raise Exception("定位不到元素")


    def input_by_number(self, label, value,index=1):
        try:
            self.input_by_index("xpath",f"//form[@class='el-form']//label[contains(text(),'{label}')]//following-sibling::div//input",value,index)
        except NoSuchElementException:
            self.logger.error(f"定位不到单行文本控件标签名:{label}")
            raise Exception("定位不到元素")

    #获取单行文本的值
    def get_text_value(self,label,index=1):
        try:
            return self.get_text_index("xpath",f"//form[@class='el-form']//label[contains(text(),'{label}')]//following-sibling::div//input",index)
        except NoSuchElementException:
            self.logger.error(f"获取值定位不到标签名:{label}")
            raise Exception("定位不到元素")
    def text_isenable(self,label,index=1):
        return self.get_enable("xpath",f"//form[@class='el-form']//label[contains(text(),'{label}')]//following-sibling::div//input",index)

    def select_by_label(self, label, value):
        try:
            self.click("xpath",f"//form[@class='el-form']//label[contains(text(),'{label}')]//following-sibling::div//input")
            self.click("xpath",f"//div[starts-with(@class,'el-select-dropdown el-popper') and not (contains(@style,'display: none'))]//span[text()='{value}']")
        except NoSuchElementException:
            self.logger.error(f"定位不到下拉框控件的标签名:{label}")
            raise Exception("定位不到元素")

    def select_by_placeholder(self, name, value):
        try:
            self.click("xpath",f"//input[@placeholder='{name}']")
            self.click("xpath", f"//div[starts-with(@class,'el-select-dropdown el-popper') and not (contains(@style,'display: none'))]//span[text()='{value}']")
        except NoSuchElementException:
            self.logger.error(f"定位不到下拉框控件的placeholder:{name}")
            raise Exception("定位不到元素")

    def select_by_placeholder_index(self,name,value,index=1):
        try:
            self.get_elements('xpath', f'//input[@placeholder="{name}"]')[index].click()
            self.click("xpath", f"//div[starts-with(@class,'el-select-dropdown el-popper') and not (contains(@style,'display: none'))]//span[text()='{value}']")
        except NoSuchElementException:
            self.logger.error(f"定位不到下拉框控件的placeholder:{name}")
            raise Exception("定位不到元素")
        #新

    def select_by_index(self, label, value,index=1):
        try:
            self.click_by_index("xpath", f"//form[@class='el-form']//label[contains(text(),'{label}')]//following-sibling::div//input",index)
            self.click("xpath", f"//div[starts-with(@class,'el-select-dropdown el-popper') and not (contains(@style,'display: none'))]//span[text()='{value}']")
        except NoSuchElementException:
            self.logger.error(f"定位不到下拉框控件的标签名:{label}")
            raise Exception("定位不到元素")


    def select_clickOption(self, value):
        try:
            self.click("xpath", f"//div[starts-with(@class,'el-select-dropdown el-popper') and not (contains(@style,'display: none'))]//span[text()='{value}']")
        except NoSuchElementException:
            self.logger.error(f"定位不到下拉框值:{value}")
            raise Exception("定位不到元素")

    '''
    申请客户、结算客户类似特殊控件实现
    传入标签名、搜索关键字、选项值
    '''
    def special_input(self,label,searchkey,name):
        try:
            self.click("xpath",f"//form[@class='el-form']//label[contains(text(),'{label}')]//following-sibling::div//button")
            self.input_by_placeholder("请输入搜索关键字",searchkey)
            self.click("xpath","//button[@class='el-button el-button--primary el-button--mini']")
            self.click("xpath",f"//tbody//span[text()='{name}']//..//..//following-sibling::td//button")
        except NoSuchElementException:
            self.logger.error(f"定位不到特殊控件标签名:{label}")
            raise Exception("定位不到元素")

    #多行文本输入
    def textarea_by_label(self, label, value):
        try:
            self.input("xpath",
                       f"//form[@class='el-form']//label[contains(text(),'{label}')]//following-sibling::div//textarea",value)
        except NoSuchElementException:
            self.logger.error(f"定位不到多行文本标签名:{label}")
            raise Exception("定位不到元素")