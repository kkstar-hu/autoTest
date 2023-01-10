import pytest_check as check
from Base.basepage import BasePage
from selenium.webdriver.common.keys import Keys
from Commons.Controls.table import Table
from Commons.Controls.text import text
import random
from NZYMS.Config import config

ret = ""
res = ""
for j in range(4):
    Letter = chr(random.randint(65, 90))  # 取大写字母 ASCII码值，对照百度
    c = str(random.choice([Letter]))
    ret += c
for i in range(8):
    num = random.randint(0, 9)
    s = str(random.choice([num]))
    ret += s
    res += s


class Send_Box_registration(BasePage):
    """
    道口管理-----送箱进场登记
    """

    def send_box_plan(self,input,boxNumber):
        """
        有计划送箱进场登记
        """
        self.logger.info('步骤1:输入已有计划的箱号')
        textInput = text(self.driver)
        textInput.input_by_number("箱号",boxNumber)
        # textInput.input_by_number("箱号", 'JX_762058')
        self.get_element('xpath', '//input[@placeholder="请输入箱号"]').send_keys(Keys.ENTER)
        self.waitloading()
        tableCheck=Table(self.driver,2)
        self.logger.info('check2：验证添加后列表的值正确')
        check.is_in(tableCheck.get_value('计划号',),f"{config.planNumber}")
        check.is_in(tableCheck.get_value("箱号"), boxNumber)
        check.is_in(tableCheck.get_value("进场作业类型"), input['进场作业类型'])
        tableCheck1 = Table(self.driver)
        check.equal(tableCheck1.get_value("尺寸"), input['尺寸'])
        check.is_in(tableCheck1.get_value("持箱人"), input['持箱人'])
    # 新


    def send_box_noplan(self, input):
        """
        无计划送箱进场登记（测试情况，结算客户 ：SHYYWL写死, 空重写死：重箱，尺寸写死：40，GP）
        """
        self.logger.info('步骤1:输入登记信息，箱号随机生产')
        textInput = text(self.driver)
        self.get_element('xpath', '//input[@placeholder="请输入箱号"]').send_keys(ret)
        self.waitloading()
        self.logger.info('步骤2:录入登记信息，数据写死')
        textInput.special_input("结算客户", "SHA", "SHAPGJHWYS/上海永旭集装箱运输")
        if input['空重'] is not None:
            textInput.select_by_label("空重", input['空重'])
        if input['尺寸'] is not None:
            textInput.select_by_placeholder("尺寸", input['尺寸'])
        if input['箱型'] is not None:
            textInput.select_by_placeholder("箱型", input['箱型'])
        if input['箱高'] is not None:
            textInput.select_by_label("箱高", input['箱高'])
        self.input('xpath', '//input[@placeholder="箱货重"]', input['箱货重'])
        if input['持箱人'] is not None:
            textInput.select_by_placeholder("请选择持箱人", input['持箱人'])
        if input['进场作业'] is not None:
            textInput.select_by_label("进场作业", input['进场作业'])
        if input['进出口'] is not None:
            textInput.select_by_label("进出口", input['进出口'])
        if input['来源'] is not None:
            textInput.select_by_label("来源", input['来源'])
        return ret

    def select_values(self, input):
        """
        道口选择功能,手机输入，车辆选择（写死了）
        """
        self.logger.info('步骤2：选择道口（进场专用/01）,车牌，手机号')
        textInput = text(self.driver)
        if input['堆场'] is not None:
            textInput.select_by_label("堆场", input["堆场"])
        if input['道口'] is not None:
            textInput.select_by_label("道口", input['道口'])
        if input['车牌'] is not None:
            textInput.select_by_label("车牌", input['车牌'])
        if input['车号'] is not None:
            self.get_element('xpath', "//input[@placeholder='请输入车号']").send_keys(input['车号'])
        if input['手机号'] is not None:
            self.get_element('xpath', '//input[@placeholder="请输入手机号"]').send_keys(input['手机号'])

    def confirm_button(self,input):
        """
        送箱确认按钮
        """
        self.logger.info('步骤3：送箱确认')
        self.get_element('xpath', "//span[text()='送箱确认']").click()
        self.check_alert(input["alert"])

    def boxs_messages(self):
        """
        箱内信息
        """
        self.get_element('xpath',
                         '//*[@id="app"]/div[3]/section/div[1]/div[2]/div[1]/div[2]/div[2]/div/div/div[2]/div/div[3]/table/tbody/tr/td[1]/div/div/input').send_keys(
            res)

    def add_box(self):
        """
        新增箱按钮
        """
        self.get_element('xpath', "//span[text()='新增箱']").click()

    def add_simple(self):
        """
        添加提单按钮
        """
        self.get_element('xpath', "//span[text()='添加提单']").click()

