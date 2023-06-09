# -*- coding:utf-8 -*-
import time
from selenium.common.exceptions import *
from selenium.webdriver import ActionChains

from Base.basepage import BasePage

class BTOS_table(BasePage):
    def __init__(self, driver, index=1):
        super(BTOS_table, self).__init__(driver)
        self.index = index

    def select_row(self, header, value):
        """
        table中点击选择行，会分页查找
        header：表头，value：值
        """
        colid = self.get_attribute_info("xpath", f"(//table[@class='vxe-table--header'])[{self.index}]//thead/tr/th//span[text()='{header}']//parent::div//parent::th","colid")
        while True:
            try:
                time.sleep(0.5)
                self.click("xpath", f"(//table[@class='vxe-table--body'])[{self.index}]//tr/td[@colid='{colid}']//span[contains(text(),'{value}') and not (contains(@style,'display: none'))]")
                time.sleep(1)
                rowid = self.get_attribute_info("xpath",f"(//table[@class='vxe-table--body'])[{self.index}]//tr/td[@colid='{colid}']//span[contains(text(),'{value}') and not (contains(@style,'display: none'))]//ancestor::tr",
                                                "rowid")
                return rowid
            except:
                if self.elementExist("xpath", "//button[@title ='下一页' and @class='vxe-pager--next-btn']"):
                    self.click("xpath", "//button[@title ='下一页' and @class='vxe-pager--next-btn']")
                else:
                    self.logger.error(f"定位不到列表头:{header}和值{value}")
                    raise Exception("定位不到元素")

    def get_value_by_rowid(self, rowid, header):
        """
        获取表格中某一格值
        header：表头 ,rowid: rowid属性值，一般和select_row方法一起用
        """
        try:
            colid = self.get_attribute_info("xpath",
                                            f"(//table[@class='vxe-table--header'])[{self.index}]//thead/tr/th//span[text()='{header}']//parent::div//parent::th",
                                            "colid")
            return self.get_text("xpath",
                                 f"(//table[@class='vxe-table--body'])[{self.index}]//tr[@rowid='{rowid}']/td[@colid='" + colid + "']//span")
        except NoSuchElementException:
            self.logger.error(f"定位不到列表头:{header}和rowid={rowid}")
            raise Exception("定位不到元素")

    def hasValue(self, header, value):
        """
        table中是否存在值
        header：表头，value：值
        return bool
        """
        colid = self.get_attribute_info("xpath", f"(//table[@class='vxe-table--header'])[{self.index}]//thead/tr/th//span[text()='{header}']//parent::div//parent::th","colid")
        while True:
            try:
                time.sleep(0.5)
                return self.elementExist("xpath", f"(//table[@class='vxe-table--body'])[{self.index}]//tr/td[@colid='{colid}']//span[contains(text(),'{value}') and not (contains(@style,'display: none'))]")
            except:
                if self.elementExist("xpath", "//button[@title ='下一页' and @class='vxe-pager--next-btn']"):
                    self.click("xpath", "//button[@title ='下一页' and @class='vxe-pager--next-btn']")
                else:
                    self.logger.error(f"定位不到列表头:{header}和值{value}")
                    raise Exception("定位不到元素")

    def click_header_button(self, name : str):
        try:
            e1 = self.get_elements_wait("xpath", f"(//div[contains(@class, 'toscom-panel')])[{self.index}]//div[@class='toscom-buttongroup']//span[text()='{name}']/..")
        except Exception:
            self.logger.error(f"定位元素失败:", exc_info=True)
        else:
            e1.click()

    def click_inner_button(self, rowid : str, name : str):
        try:
            e1 = self.get_elements_wait("xpath", f"(//div[contains(@class, 'toscom-panel')])[{self.index}]//tr[@rowid='{rowid}']//span[text()='{name}']/..")
        except Exception:
            self.logger.error(f"定位元素失败:", exc_info=True)
        else:
            e1.click()

    def get_value(self, header, row=1):
        try:
            colid = self.get_attribute_info("xpath",
                                            f"(//table[@class='vxe-table--header'])[{self.index}]//thead/tr/th//span[text()='{header}']//parent::div//parent::th",
                                            "colid")
            return self.get_text("xpath",
                                 f"(//table[@class='vxe-table--body'])[{self.index}]//tr[{row}]/td[@colid='" + colid + "']//span")
        except Exception:
            self.logger.error(f"定位元素失败:", exc_info=True)

    # 获取最后一行的单元格的值
    def get_last_row_value(self, header):
        try:
            colid = self.get_attribute_info("xpath",
                                            f"(//table[@class='vxe-table--header'])[{self.index}]//thead/tr/th//span[text()='{header}']//parent::div//parent::th",
                                            "colid")
            return self.get_text("xpath",
                                 f"(//table[@class='vxe-table--body'])[{self.index}]//tr[last()]/td[@colid='" + colid + "']//span")
        except NoSuchElementException:
            self.logger.error(f"定位不到列表头:{header}")
            raise Exception("定位不到元素")

    # 列表中选择行传入表头和值，会分页查找,点击修改按钮
    def click_edit(self, header, value):
        try:
            rowid = self.select_row(header, value)
            self.click("xpath",
                       f"(//table[@class='vxe-table--body'])[{self.index + 1}]//tr[@rowid='" + rowid + "']//div[@id='edit']")
        except NoSuchElementException:
            self.logger.error(f"定位不到列表头:{header}和值{value}")
            raise Exception("定位不到元素")

    # 存在勾选框
    def check(self, header, value):
        try:
            rowid = self.select_row(header, value)
            self.click("xpath",
                       f"(//table[@class='vxe-table--body'])[{self.index}]//tr[@rowid='" + rowid + "']/td//span[@class='vxe-cell--checkbox']")
        except NoSuchElementException:
            self.logger.error(f"定位不到列表头:{header}和值{value}")
            raise Exception("定位不到元素")

    # 列表中选择行传入表头和值，会分页查找,点击执行按钮
    def click_excute(self, header, value):
        try:
            rowid = self.select_row(header, value)
            self.click("xpath",
                       f"(//table[@class='vxe-table--body'])[{self.index + 1}]//tr[@rowid='" + rowid + "']//div[@id='execute']")
        except NoSuchElementException:
            self.logger.error(f"定位不到列表头:{header}和值{value}")
            raise Exception("定位不到元素")

    # 列表中选择行传入表头和值，会分页查找,点击更多按钮
    def click_more(self, header, value):
        rowid = self.select_row(header, value)
        self.click("xpath",
                   f"(//table[@class='vxe-table--body'])[{self.index + 1}]//tr[@rowid='" + rowid + "']//ul[@role='menubar']")

    def input_by_rowid(self, rowid, header, value):
        try:
            colid = self.get_attribute_info("xpath",
                                            f"(//table[@class='vxe-table--header'])[{self.index}]//thead/tr/th//span[text()='{header}']//parent::div//parent::th",
                                            "colid")
            self.input("xpath",
                       f"(//table[@class='vxe-table--body'])[{self.index}]//tr[@rowid='{rowid}']/td[@colid='" + colid + "']//input",
                       value)
        except NoSuchElementException:
            self.logger.error(f"定位不到列表头:{header}和值{value}")
            raise Exception("定位不到元素")

    # 根据表头输入第row行的值
    def input_by_row(self, header, value, row=1):
        try:
            colid = self.get_attribute_info("xpath",
                                            f"(//table[@class='vxe-table--header'])[{self.index}]//thead/tr/th//span[text()='{header}']//parent::div//parent::th",
                                            "colid")
            self.input_no_clear("xpath",
                       f"(//table[@class='vxe-table--body'])[{self.index}]//tr[{row}]/td[@colid='" + colid + "']//input",
                       value)
        except NoSuchElementException:
            self.logger.error(f"定位不到列表头:{header}和值{value}")
            raise Exception("定位不到元素")

    def input_select_by_row(self, header, value, row=1):
        try:
            colid = self.get_attribute_info("xpath",
                                            f"(//table[@class='vxe-table--header'])[{self.index}]//thead/tr/th//span[text()='{header}']//parent::div//parent::th",
                                            "colid")
            self.click("xpath",
                       f"(//table[@class='vxe-table--body'])[{self.index}]//tr[{row}]/td[@colid='" + colid + "']//input")
            self.click("xpath", f"//div[@class='el-scrollbar']//span[text()='{value}']")
        except NoSuchElementException:
            self.logger.error(f"定位不到列表头:{header}和值{value}")
            raise Exception("定位不到元素")

    # 列表里选行点击修改按钮row从1开始
    def editButton(self, row):
        self.click("xpath", f"(//table[@class='vxe-table--body'])[{self.index}]/tbody//tr[{row}]//div[@id='edit']")

    # 列表里选行点击执行按钮
    def excuteButton(self, row):
        self.click("xpath",
                   f"(//table[@class='vxe-table--body'])[{self.index}]/tbody//tr[{row}]//div[@id='execute']")

    # 列表里选行点击...按钮
    def moreButton(self, row=1):
        self.click("xpath",
                   f"(//table[@class='vxe-table--body'])[{self.index}]/tbody//tr[{row}]//ul[@role='menubar']")

    # 点...弹出点击执行按钮
    def menu_excute(self):
        self.click("xpath",
                   "//div[@class='el-menu--horizontal tos-el-menu__button__submenu' and not (contains(@style,'display: none'))]//ul[@role='menu']//li[@role='menuitem']//span[text()='执行']")

    # 点...弹出点击关闭按钮
    def menu_close(self):
        self.click("xpath",
                   "//div[@class='el-menu--horizontal tos-el-menu__button__submenu' and not (contains(@style,'display: none'))]//ul[@role='menu']//li[@role='menuitem']//span[text()='关闭']")

    # 点...弹出点击取消按钮
    def menu_cancel(self):
        self.click("xpath",
                   "//div[@class='el-menu--horizontal tos-el-menu__button__submenu' and not (contains(@style,'display: none'))]//ul[@role='menu']//li[@role='menuitem']//span[text()='取消']")

    # 点...弹出点击完成按钮
    def menu_complete(self):
        self.click("xpath",
                   "//div[@class='el-menu--horizontal tos-el-menu__button__submenu' and not (contains(@style,'display: none'))]//ul[@role='menu']//li[@role='menuitem']//span[text()='完成']")

    # 表格内打钩
    def tick_off_box(self, row):
        self.click("xpath",
                   f"(//table[@class='vxe-table--body'])[{self.index}]/tbody/tr[{row}]//span[@class='vxe-checkbox--icon vxe-icon-checkbox-unchecked']")

    # 点击向上排序箭头
    def up_arrow_sort(self, header):
        self.click("xpath",
                   f"//table[@class='vxe-table--header']//th//span[text()='{header}']//following-sibling::span/i[@title='升序：最低到最高']")

    # 点击向下排序箭头
    def down_arrow_sort(self, header):
        self.click("xpath",
                   f"//table[@class='vxe-table--header']//th//span[text()='{header}']//following-sibling::span/i[@title='降序：最高到最低']")
