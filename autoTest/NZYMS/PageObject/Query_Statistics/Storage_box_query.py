from Base.basepage import BasePage
from Commons.Controls.table import Table
from Commons.Controls.text import text
from NZYMS.Config import config


class Storage_Box_Query(BasePage):
    """
    存场箱查询页面操作
    """
    def select_body(self,input):
        """
        选择结算主体并检索
        """
        self.logger.info('步骤1：输入结算主体并检索')
        textInput = text(self.driver)
        textInput.click('xpath',"//span[text()='更多']")
        if input['结算主体'] is not None:
            textInput.select_by_label('结算主体',input['结算主体'])
        if input['箱号'] is not None:
            textInput.input_by_label('箱号',config.boxNumberOutPlan)
        self.waitloading()
        self.click('xpath',"//span[text()='检索']")

    def get_information(self,index=1):
        """
        通过对列表循环，查找箱子信息
        结合成字典返回
        """
        pax = []
        att = []
        a = []
        # 根据table xpath定位到表格

        table = self.get_elements('xpath',"//table[@class='vxe-table--header']")[index]
        # # 通过标签名获取表格的所有行
        table_tr_list = self.get_elements('xpath',"//tr")
        #
        # #  按行查询表格的数据，取出的数据是一整行，按,分隔每一列的数据
        for tr in table_tr_list:
            att = (tr.text).split("\n")
            pax.append(att)
        for i in pax:
            a.append(i)
        b = dict(zip(a[2],a[3]))
        config.dict = b









