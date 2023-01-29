from selenium.common import NoSuchElementException

from Base.basepage import BasePage
from Commons.log import getlogger


class Tag(BasePage):

    def closeTag(self,tagname):
        self.click("xpath", "//div[@id='tags-view-container']//span[contains(text(),'"+tagname+"')]/span")
        self.waitloading()


    def closeChoiceTag(self,tagname):
        self.right_click("xpath", f"//div[@id='tags-view-container']//span[contains(text(),'{tagname}')]")
        self.click("xpath", "//ul[@class='contextmenu']/li[text()='关闭所有']")
        self.refresh()
        self.waitloading()

    def closeTagGtos(self,tagname):
        self.click("xpath", "//div[@id='tags-view-container']//span[contains(text(),'"+tagname+"')]//following-sibling::span")
        self.waitloading()