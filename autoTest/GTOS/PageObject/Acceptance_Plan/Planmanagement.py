from Base.basepage import BasePage
from GTOS.Controls.text import Gtos_text
from GTOS.Config import config


class PlanManagement(BasePage):
    """
    计划受理--计划管理
    """
    def select_value(self,boxnumber):
        """
        输入船名航次
        """
        self.logger.info('步骤1：输入船名航次')
        textinput = Gtos_text(self.driver)
        # textinput.input_noclear_placeholder_click('请输入关键词',input['船名航次'])
        textinput.search_select_by_label('船名航次',config.importNumber)
        textinput.input_by_label('箱号',boxnumber)

    def retrieve(self):
        """
        检索
        """
        self.logger.info('步骤2：检索数据')
        self.click('xpath',"//span[text()='检索']")

    def viewing_Plan(self):
        """
        查看计划
        """
        self.logger.info('步骤3：查看计划')
        self.click('xpath',"//div//span[text()='查看计划']")
        self.get_tr_value()

    def get_tr_value(self):
        """
        获取数据内容，返回 箱预约号
        """
        pax_name = []
        att = []
        a = []
        # 通过标签名获取表格的所有行
        table_name = self.get_elements('xpath',"//div[@class='el-table el-table--fit el-table--border el-table--scrollable-x el-table--enable-row-transition el-table--medium']")
        #  按行查询表格的数据，取出的数据是一整行，按,分隔每一列的数据
        for tr in table_name:
            # print(tr.text)     获取文本
            # print(tr.get_attribute('outerHTML'))   #获取当前元素源代码
            # print(tr.is_displayed())      #判断元素文本是不是被隐藏了
            # print(tr.get_attribute('attributeName'))
            # print(tr.get_attribute('textContent'))           #获取隐藏的文本信息
            # print(tr.get_attribute('innerText').replace('  ','').replace('\n',','))          #获取隐藏的文本信息
            att = (tr.text.replace('\n',',').replace(' ',','))
            pax_name.append(att.split(','))
            for i in pax_name:
                j = i[:11]
                k = i[11:]
                a = dict(zip(j,k))
                config.Number = a['箱预约号']
                return config.Number


    def process(self,boxnumber):
        """
        流程
        """
        self.select_value(boxnumber)
        self.retrieve()
        self.viewing_Plan()



