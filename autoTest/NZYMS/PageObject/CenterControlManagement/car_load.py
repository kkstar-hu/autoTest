import time

from selenium.common import NoSuchElementException

from Base.basepage import BasePage
from Commons.Controls.text import text
from NZYMS.Config import config


class Car_Load(BasePage):
    """
    中控管理---车载
    """

    def type_of_job(self, input):
        """作业类型"""
        textInput = text(self.driver)
        if input['堆场'] is not None:
            textInput.select_by_placeholder("请选择", input["堆场"])
        self.click("xpath", "//span[text()='确认 ']")
        self.logger.info('步骤1：选择作业类型')
        try:
            self.click("xpath", f"//div[text()='{input['操作']}']")
        except NoSuchElementException:
            raise Exception("定位不到元素")
        if input['操作'] == '查找指令':
            if input['空重'] == '空箱':
                self.click("xpath", "//span[text()='空箱']")
                self.click("xpath", "//span[text()='确认 ']")
            if input['空重'] == '重箱':
                self.click("xpath", "//span[text()='重箱']")
                self.click("xpath", "//span[text()='确认 ']")
        if input['操作'] == '转堆':
            if input['空重'] == '空箱':
                self.click("xpath", "//span[text()='空箱']")
                self.click("xpath", "//span[text()='确认 ']")
            if input['空重'] == '重箱':
                self.click("xpath", "//span[text()='重箱']")
                self.click("xpath", "//span[text()='确认 ']")

    def changeStore(self, storeDump,boxType):
        textInput = text(self.driver)
        textInput.select_by_label("堆场",storeDump)
        self.click("xpath", "//span[text()='确认 ']")
        self.click("xpath", "//div[@class='yms__fork__btn__group']//div[@class='yms__fork__btn__group__item__label'][text()='转堆']")
        if boxType == "重箱":
            self.click("xpath","//div[@role='radiogroup']/label/span[contains(text(),'重箱')]")
        elif boxType == "空箱":
            self.click("xpath","//div[@role='radiogroup']/label/span[contains(text(),'空箱')]")
        self.click("xpath", "//span[text()='确认 ']")

    #先切换到新窗口
    def switchNewWindow(self):
        self.switchWindow(1)

    def closeWindow(self):
        self.driver.close()

    def choice_car(self,boxNumber,index=1):
        """
        通过选取箱号，选到框架
        """
        self.logger.info('车载：选车落箱')
        for i in range(1,20):
            if self.elementExist("xpath", f"//div[text()=' {boxNumber} ']") is False:
                self.click('xpath', "//div[@class='yms__fork__btn__right']")
            else:
                self.click('xpath', f"(//div[@class='main']//div[text()=' {boxNumber} '])[{index}]")
                break
        self.waitloading()
        time.sleep(1)


    #转推箱
    def change_box(self):
        """
        通过选取箱号，选到框架
        """
        self.logger.info('车载：选起始箱区')
        self.click('xpath', "//div[@class = 'containerGrid containerGrid-arr-light-loc containerGrid-border']")
        self.logger.info('车载：选目标箱区')
        self.waitloading()
        self.click('xpath',"(//div[@class='transfer el-row']/div[2]//span[@data-tier-no and @data-row-no]//div[@class='gridItemC gridItemC-cs']/div[1][text()=' '])[1]//parent::div")
        self.check_alert(None)


    # 放箱，自动从1-1位选空位
    def place_box(self):
        """
        通过选取箱号，选到框架
        """
        self.logger.info('车载：落箱')
        self.click('xpath',"(//div[@class='bayCon']//span[@data-tier-no and @data-row-no]//div[@class='gridItemC gridItemC-cs']/div[1][text()=''])[1]//parent::div")
        self.click('xpath', "//span[text()='确认 ']")
        self.check_alert(None)
        time.sleep(1)

    def cycle_choice_box(self,input):
        """
        循环选择箱子
        """
        for falg in range(0,101):
            xt = self.get_text_index('xpath', '//span[@class="containerBox"]', falg)
            if xt[1] == '-':
                self.click_by_index('xpath', '//span[@class="containerBox"]', falg)
                break
        self.click('xpath', "//span[text()='确认 ']")
        if self.get_alert_text() == None :
            self.driver.close()
        else:
            self.logger.info(self.get_alert_text())
            self.driver.close()


    def container_Box(self,input):
        """
        定位格子放箱子
        """
        self.click('xpath',"//div[@class = 'containerGrid containerGrid-light-loc containerGrid-arr-light-loc containerGrid-border']")
        #self.click('xpath',"(//span[@data-tier-no and @data-row-no]//div[@class='gridItemC gridItemC-cs']/div[1][text()=' '])[1]//parent::div")
        self.click('xpath', "//span[text()='确认 ']")
        self.check_alert(None)








