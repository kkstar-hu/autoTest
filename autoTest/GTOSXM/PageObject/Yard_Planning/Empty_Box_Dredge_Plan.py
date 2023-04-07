import random
import re
import time
import pytest_check as check
from Base.basepage import BasePage
from GTOSXM.Controls.text import Gtos_text
from GTOSXM.Config import configinterface
from GTOSXM.Controls.Gtos_table import Gtos_table


class Empty_Box_Dredge_Plan(BasePage):
    """
    安排空箱输运计划
    """

    def addplan(self):
        """
        新增计划
        """
        self.logger.info('新增计划')
        self.click('x', "//span[text()='新增']")

    def input_values(self, name, input, number=1):
        """
        依据name，选择输入内容
        """
        self.click('x', f"//span[text()='{name}']/parent::*/span/span[@class='el-radio__inner']")
        if name == '码头选箱':
            self.wharf_box(name, input, number)
        if name == '指定选箱':
            self.specify_box(input)

    def wharf_box(self, name, input, number=1):
        """
        码头选箱
        """
        self.logger.info('码头选箱：输入内容')
        Gtextinput = Gtos_text(self.driver)
        Gtextinput.select_by_label('尺寸', input['尺寸'])
        if input['箱型'] is not None:
            Gtextinput.select_by_label('箱型', input['箱型'])
        if input['箱高'] is not None:
            Gtextinput.select_by_label('箱高', input['箱高'])
        if input['船名航次'] is not None:
            Gtextinput.select_by_label('船名航次', input['船名航次'])
        if input['持箱人'] is not None:
            Gtextinput.select_by_label('持箱人', input['持箱人'])
        if input['贸易类型'] is not None:
            Gtextinput.select_by_label('贸易类型', input['贸易类型'])
        if input['坏/污'] is not None:
            Gtextinput.select_by_label('坏/污', input['坏/污'])
        if input['附加操作'] is not None:
            Gtextinput.select_by_label('附加操作', input['附加操作'])
        if input['外集卡组'] is not None:
            Gtextinput.select_by_label('外集卡组', input['外集卡组'])
        self.click('x', "//span[text()='生成用箱需求']")
        Gtable = Gtos_table(self.driver, 3)
        Gtable.check('尺寸', input['尺寸'])
        check.equal(Gtable.get_value('尺寸'), input['尺寸'])
        if input['箱型'] is not None:
            check.equal(Gtable.get_value('箱型'), input['箱型'])
        if input['箱高'] is not None:
            check.equal(Gtable.get_value('箱高'), input['箱高'])
        if input['船名航次'] is not None:
            check.equal(Gtable.get_value('船名航次'), input['船名航次'])
        if input['持箱人'] is not None:
            check.equal(Gtable.get_value('持箱人'), input['持箱人'])
        if input['贸易类型'] is not None:
            check.equal(Gtable.get_value('贸易类型'), input['贸易类型'])
        if input['坏/污'] is not None:
            check.equal(Gtable.get_value('坏/污'), input['坏/污'])
        if input['附加操作'] is not None:
            check.equal(Gtable.get_value('附加操作'), input['附加操作'])
        if input['外集卡组'] is not None:
            check.equal(Gtable.get_value('外集卡组'), input['外集卡组'])
        self.click('x', "//span[text()='设置计划数量']")
        self.input_no_clear('x', "//input[@placeholder='请输入数量']", number)
        check.equal(Gtable.get_value('计划数量'), f'{number}')
        self.click('x', "(//div[@id='add']//span[text()='新增'])[2]")
        self.left_click('x', "((//div[@class='ag-center-cols-container'])[4]//input)[1]")
        self.click('x', "//span[text()='AUTOTEST']")
        self.left_clickandsend('x', "((//div[@class='ag-center-cols-container'])[4]//input)[2]", '1')
        self.click('x', "(//span[text()='保存'])[1]")
        self.logger.info('码头选箱获取信息：' + self.get_text("xpath", "//div[@role='alert']//p"))
        a = self.get_text("xpath", "//div[@role='alert']//p")
        code = re.search(r'\d+$', a).group()  # 提取数字
        self.logger.info('码头选箱提取预约号：' + code)
        self.left_clickandsend('x', "//input[@aria-label='预约号 Filter Input']", code)
        Gtable1 = Gtos_table(self.driver)
        Gtable1.check('预约号', code)
        check.equal(Gtable1.get_value('选箱模式'), name)
        self.logger.info('码头选箱：添加选箱范围')
        self.left_click('x', "//span[text()='选箱']")
        time.sleep(1)
        self.left_clickandsend('x', "//input[@aria-label='箱区 Filter Input']", 'Q9')
        time.sleep(1)
        self.left_click('x', "(//div[@class='nzctos-grid__selection_buttons']//span[text()='全'])[3]")
        self.logger.info('码头选箱：保存内容')
        self.click('x', "//span[text()='保 存']")
        self.click('x', "//span[contains(text(),'确定')]")
        self.check_alert('保存成功')
        self.close_alert('保存成功')

    def specify_box(self, input):
        """
        指定选箱
        """
        self.logger.info('指定选箱：输入内容')
        self.click('x', "//span[text()='高级']")
        Gtextinput = Gtos_text(self.driver)
        if input['箱区'] is not None:
            Gtextinput.search_select_by_label('箱区', input['箱区'])
        if input['起始倍'] is not None:
            Gtextinput.select_by_label('起始倍', input['起始倍'])
        if input['终止倍'] is not None:
            Gtextinput.select_by_label('终止倍', input['终止倍'])
        if input['尺寸'] is not None:
            Gtextinput.select_by_index('尺寸', input['尺寸'], 2)
        if input['箱高'] is not None:
            Gtextinput.select_by_index('箱高', input['箱高'], 2)
        if input['箱状态'] is not None:
            Gtextinput.select_by_label('箱状态', input['箱状态'])
        if input['扣留'] is not None:
            Gtextinput.select_by_label('扣留', input['扣留'])
        if input['坏/污'] is not None:
            Gtextinput.select_by_index('坏/污', input['坏/污'], 2)
        if input['码头放行'] is not None:
            Gtextinput.select_by_label('码头放行', input['码头放行'])
        if input['附加操作'] is not None:
            Gtextinput.select_by_index('附加条件', input['附加操作'], 2)
        if input['卸货港'] is not None:
            Gtextinput.select_by_label('卸货港', input['卸货港'])
        if input['作业方式'] is not None:
            Gtextinput.select_by_label('作业方式', input['作业方式'])
        if input['贸易类型'] is not None:
            Gtextinput.select_by_index('贸易类型', input['贸易类型'], 2)
        if input['持箱人'] is not None:
            Gtextinput.select_by_index('持箱人', input['持箱人'], 2)
        if input['装船船名航次'] is not None:
            Gtextinput.select_by_label('装船船名航次', input['装船船名航次'])
        if input['卸船船名航次'] is not None:
            Gtextinput.select_by_label('卸船船名航次', input['卸船船名航次'])
        if input['箱号'] is not None:
            Gtextinput.select_by_label('箱号', input['箱号'])
        self.click('x', "//div[@class='nzctos-buttongroup']//span[text()='检索']")
        self.logger.info('指定选箱：选择指定箱')
        configinterface.boxNumber = self.give_list()
        self.left_clickandsend('x', "//input[@aria-label='箱号 Filter Input']", configinterface.boxNumber)
        Gtable = Gtos_table(self.driver, 5)
        Gtable.tick_off_box(1)
        self.click('x', "//span[text()='添加到箱清单']")
        self.logger.info('指定选箱：选择流向')
        Gtable1 = Gtos_table(self.driver, 6)
        check.equal(Gtable1.get_value('流向'), '')
        check.equal(Gtable1.get_value('箱号'), configinterface.boxNumber)
        Gtable1.tick_off_box(1)
        self.click('x', "//span[text()='指定流向']")
        Gtextinput.select_by_label('流向', 'AUTOTEST')
        self.click('x', "//span[text()='保 存']")
        check.equal(Gtable1.get_value('流向'), '自动化流向')
        self.click('x', "(//span[text()='保存'])[2]")
        self.logger.info('指定选箱获取信息：' + self.get_text("xpath", "//div[@role='alert']//p"))
        a = self.get_text("xpath", "//div[@role='alert']//p")
        code = re.search(r'\d+$', a).group()  # 提取数字
        self.logger.info('指定选箱提取预约号：' + code)
        self.left_clickandsend('x', "//input[@aria-label='预约号 Filter Input']", code)
        Gtable3 = Gtos_table(self.driver)
        check.equal(Gtable3.get_value('可用'), '启用')

    def give_list(self):
        """
        获取可用箱号列表,并随机获取一个可用的箱号
        """
        boxid = []
        coldid = self.get_attribute_info('x',
                                         "(//div[@class='ag-header-container'])[5]//span[@ref='eText' and text("
                                         ")='箱号']//parent::div//parent::div//parent::div",
                                         'col-id')
        a = self.get_elements("xpath", f"(//div[@class='ag-center-cols-container'])[5]//div[@col-id='" + coldid + "']")
        # 获取当前可使用的所有箱号，并加入列表
        for i in a:
            boxid.append(i.get_attribute('innerText'))
        b = random.choice(boxid)  # 随机选择其中一个箱号

        return b
