# -*- coding:utf-8 -*-
import time
import allure
import pytest_check as check

from BTOSLJ.Config import config
from Base.basepage import BasePage
from BTOSLJ.Config.config import mydata
from BTOSLJ.Controls.BTOS_text import BtosText
from BTOSLJ.Controls.BTOS_table import BTOS_table
from Commons.DateTime import DataTime

class ShipDate(BasePage):
    '''
        船期操作
    '''
    def __init__(self, driver):
        super(ShipDate, self).__init__(driver)
        self.scd_eta = DataTime.Get_Current_Time_Format()   # 计划抵港时间/计划靠泊时间
        self.scd_etd = DataTime.Get_Date_X_Number_Of_Days(2) + " 00:00:00"  # 计划离港时间/计划离泊时间
        self.textInput = BtosText(self.driver)
        self.table = BTOS_table(self.driver, 1)
        self.rowid = None

    # 新增船期
    @allure.step("新增船期")
    def add_schedule(self, input : dict):
        self.logger.info("新增船期")
        self.click("id", "add")
        self.textInput.select_by_label_drawer("船舶代码", input["船舶代码"], 0.5)
        self.textInput.select_by_label_drawer("上一港", input["上一港"])
        self.textInput.select_by_label_drawer("下一港", input["下一港"])
        self.textInput.input_time_by_label_drawer("计划抵港时间", self.scd_eta)
        self.textInput.input_time_by_label_drawer("计划离港时间", self.scd_etd)
        self.textInput.input_text_by_label_drawer("航次", config.importNumber)
        self.textInput.select_by_label_drawer("航线", input["航线"])
        self.textInput.mul_select_by_label_drawer("货名", input["货名"])
        self.textInput.input_by_for_drawer("bpsIvoyageQuery.scdIton", input["总吨"])
        self.textInput.select_by_label_drawer("船代", input["船代"], 0.5)
        self.textInput.input_text_by_label_drawer("船代联系人", input["船代联系人"])
        self.textInput.select_by_label_drawer("贸易类型", input["贸易类型"])
        self.textInput.click("xpath", "//span[text()='保存并关闭']")
        #self.element_wait("xpath", "//div[@role='alert']//p")
        self.check_alert_and_close("新增成功")

    # 检查数据
    @allure.step("检查数据")
    def check_schedule(self, input : dict):
        #self.textInput.select_by_label_correct("船名", input["船舶代码"], 0.5)
        #self.click('xpath', "//span[contains(text(),'检索')]")
        self.rowid = self.table.select_row("进口航次", config.importNumber)
        check.equal(self.table.get_value_by_rowid(self.rowid, '中文船名'), mydata.vsl_cnname)
        check.equal(self.table.get_value_by_rowid(self.rowid, '英文船名'), mydata.vsl_enname)
        check.equal(self.table.get_value_by_rowid(self.rowid, '船期状态'), '预报')
        check.equal(self.table.get_value_by_rowid(self.rowid, '计划抵港时间'), self.scd_eta)

    # 确报
    @allure.step("确报")
    def confirm_arrive(self, input : dict):
        self.logger.info("确报")
        self.table.click_header_button("确报")
        self.check_alert_and_close("确报成功")
        self.rowid = self.table.select_row("进口航次", config.importNumber)
        check.equal(self.table.get_value_by_rowid(self.rowid, '船期状态'), '确报')

    # 再次确报
    @allure.step("再次确报")
    def confirm_arrive_2(self, input : dict):
        self.logger.info("再次确报")
        self.table.click_header_button("确报")
        self.check_alert_and_close("只有预报的船期可以确报")
        self.rowid = self.table.select_row("进口航次", config.importNumber)
        check.equal(self.table.get_value_by_rowid(self.rowid, '船期状态'), '确报')

    # 分区
    @allure.step("分区")
    def divide_region(self, input : dict):
        self.logger.info("分区")
        self.table.click_header_button("分区")
        self.get_elements_wait("xpath", "//span[contains(text(), '保存')]").click()
        self.check_alert_and_close("分区成功")
        self.rowid = self.table.select_row("进口航次", config.importNumber)
        check.equal(self.table.get_value_by_rowid(self.rowid, '作业区'), '罗泾')

    # 再次分区
    @allure.step("再次分区")
    def divide_region_2(self, input : dict):
        self.logger.info("再次分区")
        self.table.click_header_button("分区")
        self.get_elements_wait("xpath", "//span[contains(text(), '保存')]").click()
        self.check_alert_and_close("只有未分区的船期可以分区")
        self.rowid = self.table.select_row("进口航次", config.importNumber)
        check.equal(self.table.get_value_by_rowid(self.rowid, '作业区'), '罗泾')

    @allure.step("新增靠泊计划")
    def add_berth_plan(self, input : dict):
        self.logger.info("新增靠泊计划")
        self.rowid = self.table.select_row("进口航次", config.importNumber)
        self.table.click_inner_button(self.rowid, "修改")
        time.sleep(0.5)
        self.get_elements_wait("xpath", "//span[text()='新增靠泊']/..").click()
        self.textInput.input_text_by_label_drawer("起始尺码", input["起始尺码"])
        self.textInput.select_by_label_drawer("靠泊方向", input["靠泊方向"])
        self.textInput.select_by_label_drawer("起始泊位", input["起始泊位"])
        self.textInput.select_by_label_drawer("终止泊位", input["终止泊位"])
        self.textInput.input_time_by_label_drawer("靠泊时间", self.scd_eta)
        self.textInput.input_time_by_label_drawer("离泊时间", self.scd_etd)
        self.textInput.input_text_by_label_drawer("靠泊吃水", input["靠泊吃水"])
        self.textInput.input_text_by_label_drawer("离泊吃水", input["离泊吃水"])
        self.textInput.mul2_select_by_label_index("船头榄桩", 1)
        self.textInput.mul2_select_by_label_index("船尾榄桩", 1)
        self.click("xpath", "//span[text()='保存并关闭']/..")
        self.check_alert_and_close("修改成功")









