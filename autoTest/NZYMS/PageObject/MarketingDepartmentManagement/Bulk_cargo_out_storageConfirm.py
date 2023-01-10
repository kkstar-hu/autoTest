from selenium.webdriver.common.by import By

from Base.basepage import BasePage
from Commons.Controls.table import Table
from Commons.Controls.text import text
from Commons.DateTime import DataTime
import pytest_check as check
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from NZYMS.Config import config


class Bulk_cargo_out_storageConfirm(BasePage):
    """
    散货入库确认
    """
    def out_carnumber(self,input):
        """
        输入车牌号
        """
        self.logger.info('步骤1：输入车牌号')
        textInput = text(self.driver)
        textInput.input_by_placeholder('请输入车牌号',input['车牌']+input['车号'])
        textInput.select_by_label("结算主体",input['结算主体'])

    def retrieve(self):
        """
        点击检索按钮
        """
        self.click('xpath', "//span[text()='检索']")

    def reset(self):
        """
        点击重置按钮
        """
        self.click('xpath', "//span[text()='重置']")

    def addbulk_out(self,input):
        """
        新增出库登记信息
        """
        try:
            self.out_carnumber(input)
            self.retrieve()
            self.logger.info(('步骤1：选择数据主题'))
            self.click('xpath', f"//span[text()='{config.bulkoutNumber}']")
            self.logger.info('步骤2：新增出库信息')
            textInput = text(self.driver)
            textInput.click('xpath', "//div[@id='add']")
            textInput.input_by_label('出库件数', int(input['出库件数']) / 2)
            textInput.input_by_label('出库体积', int(input['出库体积']) / 2)
            textInput.input_by_label('出库重量(kg)', int(input['出库重量(kg)']) / 2)
            self.element_wait_disappear(By.XPATH, "//div[@role='alert']//p")
            self.save_and_close()
            createTime = DataTime.GetTime()
            self.logger.info('check1：验证入库明细弹出提示信息')
            self.check_alert(input["addboxconfirm"])
        except:
            self.click("xpath", "//button//span[text()='取消 ']")
        tableCheck = Table(self.driver,3)
        self.logger.info('check3：验证添加后列表的值正确')
        check.equal(tableCheck.get_value("出库件数"), str(int(input['出库件数']) // 2))
        check.equal(tableCheck.get_value("出库体积"), str(int(input['出库体积']) // 2))
        check.equal(tableCheck.get_value("出库重量(kg)"), str(int(input['出库重量(kg)']) // 2))
        check.less(DataTime.get_dif_time(tableCheck.get_value("登记时间"), createTime), 300)
        check.equal(tableCheck.get_value("登记人"), config.createName)
