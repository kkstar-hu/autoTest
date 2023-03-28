from Base.basepage import BasePage

class Tag(BasePage):

    #关闭tag页
    def closeTag(self,tagname):
        self.click("xpath", "//div[@id='tags-view-container']//span[contains(text(),'"+tagname+"')]/span")
        self.waitloading()

    # 关闭所有tag页
    def closeChoiceTag(self,tagname):
        self.right_click("xpath", f"//div[@id='tags-view-container']//span[contains(text(),'{tagname}')]")
        self.click("xpath", "//ul[@class='contextmenu']/li[text()='关闭所有']")
        self.refresh()
        self.waitloading()

    #GTOS里关闭tag页
    def closeTagGtos(self,tagname):
        self.click("xpath", "//div[@id='tags-view-container']//span[contains(text(),'"+tagname+"')]//following-sibling::span")
        self.waitloading()