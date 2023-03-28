from selenium.common import NoSuchElementException
from selenium.webdriver import ActionChains
from Base.basepage import BasePage
from Commons.log import getlogger


class Gtos_table(BasePage):

    def __init__(self,driver,index=1):
        """
        运行初始化方法，index 页面中第几个table
        """
        self.driver = driver
        self.logger = getlogger()
        self.index=index

    def get_value(self,header,row=1):
        """
        获取表格中某一格值
        header：表头 ,row:行号
        """
        try:
            colid=self.get_attribute_info("xpath",f"(//div[@class='ag-header-container'])[{self.index}]//span[@ref='eText' and text()='{header}']//parent::div//parent::div//parent::div","col-id")
            return self.get_attribute_info("xpath",f"(//div[@class='ag-center-cols-container'])[{self.index}]/div[{row}]/div[@col-id='"+colid+"']",'textContent')
        except NoSuchElementException:
            self.logger.error(f"定位不到列表头:{header}")
            raise Exception("定位不到元素")

    def get_value_by_rowid(self,rowid,header):
        """
        获取表格中某一格值
        header：表头 ,rowid: rowid属性值，一般和select_row方法一起用
        """
        try:
            colid=self.get_attribute_info("xpath",f"(//div[@class='ag-header-container'])[{self.index}]//span[@ref='eText' and text()='{header}']//parent::div//parent::div//parent::div","col-id")
            return self.get_attribute_info("xpath",
                                 f"(//div[@class='ag-center-cols-container'])[{self.index}]//div[@row-id='{rowid}']/div[@col-id='" + colid + "']",'textContent')
        except NoSuchElementException:
            self.logger.error(f"定位不到列表头:{header}和rowid={rowid}")
            raise Exception("定位不到元素")

    def get_last_row_value(self,header):
        """
        获取最后一行的某单元格的值
        header：表头
        """
        try:
            colid=self.get_attribute_info("xpath",f"(//div[@class='ag-header-container'])[{self.index}]//span[@ref='eText' and text()='{header}']//parent::div//parent::div//parent::div","col-id")
            return self.get_attribute_info("xpath",f"(//div[@class='ag-center-cols-container'])[{self.index}]//div[last()]/div[@col-id='"+colid+"']",'textContent')
        except NoSuchElementException:
            self.logger.error(f"定位不到列表头:{header}")
            raise Exception("定位不到元素")

    def select_row(self, header, value):
        """
        table中点击选择行，会分页查找
        header：表头，value：值
        """
        try:
            colid=self.get_attribute_info("xpath",f"(//div[@class='ag-header-container'])[{self.index}]//span[@ref='eText' and text()='{header}']//parent::div//parent::div//parent::div","col-id")
            self.left_click("xpath",f"(//div[@class='ag-center-cols-container'])[{self.index}]//div[@col-id='" + colid + "' and text()='" + value + "']")
            rowid = self.get_attribute_info("xpath",f"(//div[@class='ag-center-cols-container'])[{self.index}]//div[@col-id='" + colid + "'][text()='" + value + "']//ancestor::div[@row-id]","row-id")
            return rowid
        except:
            self.logger.error(f"定位不到列表头:{header}和值{value}")
            raise Exception("定位不到元素")

    def left_select(self,header):
        try:
            e1 = self.get_element("xpath",f"(//div[@class='ag-pinned-left-cols-container'])[{self.index}]//div//div[contains(text(),'{header}')]")
            ActionChains(self.driver).click(e1).perform()
        except:
            self.logger.error(f"定位不到列表头:{header}")
            raise Exception("定位不到元素")

    def select_row2(self, header, value):
        """
        列表存在右侧箭头使用此方法
        table中点击选择行，会分页查找
        header：表头，value：值
        """
        try:
            colid=self.get_attribute_info("xpath",f"(//div[@class='ag-header-container'])[{self.index}]//span[@ref='eText' and text()='{header}']//parent::div//parent::div//parent::div","col-id")
            self.left_click("xpath",f"(//div[@class='ag-center-cols-container'])[{self.index}]//div[@col-id='" + colid + "']//span[text()='" + value + "']")
            rowid = self.get_attribute_info("xpath",f"(//div[@class='ag-center-cols-container'])[{self.index}]//div[@col-id='" + colid + "']//span[text()='" + value + "']//ancestor::div[@row-id]","row-id")
            return rowid
        except:
            self.logger.error(f"定位不到列表头:{header}和值{value}")
            raise Exception("定位不到元素")

    def check(self,header,value):
        """
        table中勾选前方勾选框，会分页查找
        header：表头，value：值
        """
        try:
            rowid = self.select_row(header,value)
            self.left_click("xpath", f"(//div[@class='ag-center-cols-container'])[{self.index}]//div[@row-id='"+rowid+"']//div[@ref='eCheckbox']")
        except:
            self.logger.error(f"定位不到列表头:{header}和值{value}")
            raise Exception("定位不到元素")

    def check2(self,header,value):
        """
        列表存在右侧箭头使用此方法
        table中勾选前方勾选框，会分页查找
        header：表头，value：值
        """
        try:
            rowid = self.select_row2(header,value)
            self.left_click("xpath", f"(//div[@class='ag-center-cols-container'])[{self.index}]//div[@row-id='"+rowid+"']//div[@ref='eCheckbox']")
        except:
            self.logger.error(f"定位不到列表头:{header}和值{value}")
            raise Exception("定位不到元素")

    #存在勾选框，左边有个固定列表
    def check_existLeftTable(self,header,value):
        try:
            rowid = self.select_row(header,value)
            self.left_click("xpath", f"(//div[@class='ag-pinned-left-cols-container'])[{self.index}]//div[@row-id='"+rowid+"']//div[@class='eCheckbox']")
        except:
            self.logger.error(f"定位不到列表头:{header}和值{value}")
            raise Exception("定位不到元素")

    #存在左边有个固定列表
    def get_value_left_table(self,header,row=1):
        try:
            colid=self.get_attribute_info("xpath",f"(//div[@class='ag-header-container'])[{self.index}]//span[@ref='eText' and text()='{header}']//parent::div//parent::div//parent::div","col-id")
            return self.get_attribute_info("xpath",f"(//div[@class='ag-pinned-left-cols-container'])[{self.index}]/div[{row}]/div[@col-id='"+colid+"']",'textContent')
        except NoSuchElementException:
            self.logger.error(f"定位不到列表头:{header}")
            raise Exception("定位不到元素")

    def tick_off_box(self,row=1):
        """
        表格内勾选前方勾选框
        row：行号
        """
        em = self.get_element('xpath',f"(//div[@class='ag-center-cols-clipper'])[{self.index}]//div[@row-index='{row-1}']//input")
        ActionChains(self.driver).move_to_element(em).click().perform()
        self.element_wait('xpath',f"(//div[@class='ag-center-cols-clipper'])[{self.index}]//div[@row-index='{row-1}']//input[@aria-label='Press Space to toggle row selection (checked)']")

    #gtos 获取弹窗类，label后面的值
    def get_body_values(self,name):
        try:
            em = self.get_element('xpath',
                              f"(//div[@class='nzctos-v-dialog__body'])//label[@class='el-form-item__label' and contains(text(),'{name}')]/following-sibling::div[@class='el-form-item__content']")
        except NoSuchElementException:
            raise Exception("定位不到元素")
        return em.text

    def Big_get_value(self,name):
        '''
        大船桥吊
        '''
        cla_ss = self.get_attribute_info('x',f"//div[@class='cell' and text()='{name}']/parent::th","class")
        cla = list(cla_ss.split(' '))[0]
        return self.get_attribute_info('x',f"//td[@class='{cla}   el-table__cell']//div//p","textContent").strip()

    def plan_get_value(self,name):
        '''
        获取计划管理内容
        '''
        cla_ss = self.get_attribute_info('x', f"//div[@class='cell' and text()='{name}']/parent::th", "class")
        cla = list(cla_ss.split(' '))
        return self.get_attribute_info('x',f"//td[@class='{cla[0]+' '+cla[2]}  el-table__cell']//div","textContent").strip()

