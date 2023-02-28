import time

import pytest_check as check
from Base.basepage import BasePage
from GTOS.Config import config
from GTOS.Controls.Gtos_table import Gtos_table
from GTOS.Controls.text import Gtos_text


class CheckInBox(BasePage):
    """
    道口管理----办理进箱手续
    """
    def search(self,input,boxNumberfirst=None,boxNumberbehind=None,boxNumbercenter=None):
        textInput = Gtos_text(self.driver)
        if input["集卡编号"] is not None:
            textInput.select_by_label("集卡编号", input["车牌"])
            self.get_element('xpath', "//input[@placeholder='请输入集卡号']").send_keys(input["集卡编号"])
        if boxNumberfirst is not None:
            textInput.input_by_label("前", boxNumberfirst)
        if boxNumberbehind is not None:
            textInput.input_by_label("中", boxNumberbehind)
        if boxNumbercenter is not None:
            textInput.input_by_label("后", boxNumbercenter)
        if input["车队"] is not None:
            textInput.select_by_label("车队", input['车队'])
        time.sleep(0.5)
        self.click("x","//button//span[text()='检索']")

    def input_checkin_info(self,input):
        self.logger.info('办理进箱手续-输入进箱信息')
        textInput = Gtos_text(self.driver)
        #航民航次
        textInput.select_by_label("出口航次", config.outportNumber)
        textInput.select_by_label("装货港", input['装货港'])
        textInput.select_by_label("卸货港", input['卸货港'])
        textInput.select_by_label("目的港", input['目的港'])
        textInput.select_by_label("箱门方向", input['箱门方向'])
        check.is_false(textInput.text_isenable("进口航次"))
        #提单信息
        textInput.select_by_label("持箱人", input['持箱人'])
        textInput.select_by_label("付费人", input['付费人'])
        #textInput.select_by_label("附加操作", input['附加操作'])
        textInput.select_by_label("箱组", input['箱组'])
        #箱信息
        textInput.input_by_label("铅封号", input['铅封号'])
        textInput.select_by_label("箱状态", input['箱状态'])
        textInput.select_by_label("贸易类型", input['贸易类型'])
        textInput.select_by_label("尺寸", input['尺寸'])
        textInput.select_by_label("箱型", input['箱型'])
        textInput.select_by_label("箱高", input['箱高'])
        check.is_false(textInput.text_isenable("ISO"))
        #验箱
        check.is_false(textInput.text_isenable("是否危险品"))
        check.is_false(textInput.text_isenable("是否超限"))
        check.is_false(textInput.text_isenable("限重"))
        check.is_false(textInput.text_isenable("是否冷藏箱"))
        #特殊信息
        textInput.select_by_label("工原残标志", input['工原残标志'])
        textInput.select_by_label("残损代码", input['残损代码'])
        textInput.select_by_label_exact("超限", input['超限'])
        if input["危类"]!=None:
            textInput.select_by_label("危类", input['危类'])
            textInput.input_by_label("UNNO", input['UNNO'])

    def click_behindbox_tag(self):
        self.click("id","TContainerNoBack")

    def click_centerdbox_tag(self):
        self.click("id", "TContainerNoMiddle")

    def addgoodsinfo(self,input, takeNumber):
        self.logger.info('办理进箱手续-新增箱货信息')
        self.click("x", "//span[text()='新增货']")
        self.waitloading()
        try:
            textInput = Gtos_text(self.driver)
            textInput.input_by_label("提单号", takeNumber)
            textInput.input_by_label("订舱号", input['订舱号'])
            textInput.select_by_label("交付方式", input['交付方式'])
            textInput.select_by_label("交货地", input['交货地'])
            textInput.input_by_label("分件数", input['分件数'])
            textInput.input_by_label("分重量", input['分重量'])
            textInput.input_by_label("分体积", input['分体积'])
            textInput.input_by_label("长度", input['长度'])
            textInput.input_by_label("宽度", input['宽度'])
            textInput.input_by_label("高度", input['高度'])
            textInput.select_by_label("货类代码", input['货类代码'])
            textInput.select_by_label("包装类型", input['包装类型'])
            if input["危类"] != None:
                textInput.select_by_index("危类", input['危类'])
                textInput.input_by_number("UNNO", input['UNNO'])
            textInput.input_by_number("温度", input['温度'],2)
            textInput.select_by_index("温度单位", input['温度单位'])
            textInput.textarea_by_label("货名", input['货名'])
            textInput.textarea_by_label("唛头", input['唛头'])
            textInput.input_by_label("发货人", input['发货人'])
            textInput.input_by_label("收货人", input['收货人'])
            self.click("x", "//button//span[text()='保 存']")
            self.check_alert(input["addgoodsalert"])
        except:
            self.cancel()
        if input["addgoodsalert"]=='保存成功':
            tableCheck=Gtos_table(self.driver)
            check.equal(tableCheck.get_value("提单号"), takeNumber)
            check.equal(tableCheck.get_value("订舱号"), input['订舱号'])
            check.equal(tableCheck.get_value("交付方式"), input['交付方式'])
            check.equal(tableCheck.get_value("交货地"), input['交货地'])
            check.equal(tableCheck.get_value("分件数"), input['分件数'])
            check.equal(tableCheck.get_value("分重量"), input['分重量'])
            check.equal(tableCheck.get_value("分体积"), input['分体积'])
            check.equal(tableCheck.get_value("长度"), input['长度'])
            check.equal(tableCheck.get_value("宽度"), input['宽度'])
            check.equal(tableCheck.get_value("高度"), input['高度'])
            check.equal(tableCheck.get_value("货类代码"), input['货类代码'])
            check.equal(tableCheck.get_value("包装类型"), input['包装类型'])
            #check.equal(tableCheck.get_value("危类"), input['危类'])
            #check.equal(tableCheck.get_value("UNNO"), input['UNNO'])
            check.equal(tableCheck.get_value("温度单位"), input['温度单位'])
            check.equal(tableCheck.get_value("温度"), input['温度'])
            check.equal(tableCheck.get_value("货名"), input['货名'])
            check.equal(tableCheck.get_value("唛头"), input['唛头'])
            check.equal(tableCheck.get_value("发货人"), input['发货人'])
            check.equal(tableCheck.get_value("收货人"), input['收货人'])


    def input_info(self,input):
        self.input("x","//span[text()='地磅重量：']//following-sibling::div[1]/input",input['地磅重量'])
        self.click("x", "//span[text()='车架类型：']//following-sibling::div//input")
        self.click("x", "//div[starts-with(@class,'el-select-dropdown el-popper') and not (contains(@style,'display: none'))]//span[contains(text(),'自卸架')]")
        self.input("x", "//span[text()='车架号：']//following-sibling::div/input", input['车架号'])
        if self.elementExist("x","//button[@class='el-button el-tooltip el-button--warning el-button--mini is-circle']"):
            pass
        else:
            self.click("x", "//span[text()='进口道口号：']//following-sibling::div//input")
            self.click("x",f"//div[starts-with(@class,'el-select-dropdown el-popper') and not (contains(@style,'display: none'))]//span[contains(text(),{input['进口道口号']})]")


    def other_information(self,input):
        """
        车门方向
        """
        textInput = Gtos_text(self.driver)
        textInput.select_by_label("箱门方向", input['箱门方向'])
        textInput.select_by_label("付费人", input['付费人'])
        time.sleep(0.5)


    def confirm_button(self,input):

        """
        送箱确认按钮
        """
        self.get_element('xpath', "//span[text()='确认进箱']").click()
        self.click("x","//button/span[text()=' 否 ']")
        self.check_alert(input["alert"])



