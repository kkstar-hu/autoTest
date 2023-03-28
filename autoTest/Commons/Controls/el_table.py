from selenium.common import NoSuchElementException

from Base.basepage import BasePage
from Commons.log import getlogger


class ELtable(BasePage):

    def __init__(self,driver,index=1):
        """
        运行初始化方法，index页面中第几个table
        """
        self.driver = driver
        self.logger = getlogger()
        self.index=index

    def get_value(self,header,row=1):
        """
        获取表格某行中某一格值
        header：表头 ,row:行号
        """
        try:
            classValueHeader=self.get_attribute_info("xpath",f"(//table[@class='el-table__header'])[{self.index}]//thead/tr/th/div[text()='{header}']//parent::th","class")
            classValue=classValueHeader.split(" ")[0]
            return self.get_text("xpath",f"(//table[@class='el-table__body'])[{self.index}]//tr[{row}]/td[contains(@class,'"+classValue+"')]//div")
        except NoSuchElementException:
            self.click("xpath", "//div[@class='itemFooter']//button//span[text()='取消']")
            self.logger.error(f"定位不到列表头:{header}")
            raise Exception("定位不到元素")


    #通过唯一的值value，header来勾选
    def select_row(self, header, value):
        try:
            classValueHeader = self.get_attribute_info("xpath",f"(//table[@class='el-table__header'])[{self.index}]//thead/tr/th/div[text()='{header}']//parent::th","class")
            classValue = classValueHeader.split(" ")[0]
            self.click("xpath",f"(//table[@class='el-table__body'])[{self.index}]//tr/td[contains(@class,'"+classValue+"')]/div[contains(text(),'"+value+"')]//parent::td//parent::tr/td[1]//span")
        except NoSuchElementException:
            self.logger.error(f"定位不到列表头:{header}和值{value}")
            raise Exception("定位不到元素")

    def get_value_by_trElement(self, header,value,getheader):
        classValueHeader = self.get_attribute_info("xpath",
                                                   f"(//table[@class='el-table__header'])[{self.index}]//thead/tr/th/div[text()='{header}']//parent::th",
                                                   "class")
        classValue = classValueHeader.split(" ")[0]
        classValueHeader2 = self.get_attribute_info("xpath",
                                                   f"(//table[@class='el-table__header'])[{self.index}]//thead/tr/th/div[text()='{getheader}']//parent::th",
                                                   "class")
        classValue2 = classValueHeader2.split(" ")[0]
        return self.get_text("xpath",
                             f"(//table[@class='el-table__body'])[{self.index}]//tr/td[contains(@class,'" + classValue + "')]/div[contains(text(),'"+value+"')]//parent::td//parent::tr/td[contains(@class,'"+classValue2+"')]/div")

    #选择第几行
    def click_row(self,row):
        try:
            self.click("xpath",f"(//table[@class='el-table__body'])[{self.index}]//tr[{row}]/td[1]//span")
        except NoSuchElementException:
            self.click("xpath","//div[@class='itemFooter']//button//span[text()='取消']")
            raise Exception("定位不到元素")

    def input_text(self, header, value, row=1):
        try:
            classValueHeader = self.get_attribute_info("xpath",
                                                       f"(//table[@class='el-table__header'])[{self.index}]//thead/tr/th/div[text()='{header}']//parent::th",
                                                       "class")
            classValue = classValueHeader.split(" ")[0]
            self.input("xpath",
                           f"(//table[starts-with(@class,'el-table__body')])[{self.index}]//tr[{row}]/td[contains(@class,'"+classValue+"')]//input",
                           value)
        except NoSuchElementException:
            self.logger.error(f"定位不到列表头:{header}和值{value}")
            raise Exception("定位不到元素")

    def input_select(self, header, value, row=1):
        try:
            classValueHeader = self.get_attribute_info("xpath",
                                                       f"(//table[@class='el-table__header'])[{self.index}]//thead/tr/th/div[text()='{header}']//parent::th",
                                                       "class")
            classValue = classValueHeader.split(" ")[0]
            self.click("xpath",
                           f"(//table[starts-with(@class,'el-table__body')])[{self.index}]//tr[{row}]/td[contains(@class,'"+classValue+"')]//input")
            self.click("xpath",
                       f"//div[starts-with(@class,'el-select-dropdown el-popper') and not (contains(@style,'display: none'))]//span[text()='{value}']")
        except NoSuchElementException:
            self.logger.error(f"定位不到列表头:{header}和值{value}")
            raise Exception("定位不到元素")

