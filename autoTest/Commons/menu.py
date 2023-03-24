import time
from Base.basepage import BasePage
from Commons.excel import Excel
import xlwings as xw


class Menu(BasePage):
    def selectMenu(self,name):
        try:
            self.element_wait("xpath","//span[text()='"+name+"']")
            self.get_element("xpath","//span[text()='"+name+"']").click()
            time.sleep(0.3)
        except:
            raise Exception(f"未找到菜单{name}")

    def select_level_Menu(self,name):
        try:
            menuName=self.get_text("xpath","//div[@id='tags-view-container']//span[@class='tags-view-item active']").strip()
            if menuName in name:
                return
            elif "," in name:
                for x in name.split(","):
                    self.selectMenu(x)
            else: self.selectMenu(name)
            self.waitloading()
            time.sleep(1)
        except:
            try:
                self.select_level_Menu(name)
            except:
                raise Exception(f"未找到菜单{name}")

    def print_Menu(self,filename,sheetname):
        tobarMenuElement=self.get_elements("x","//div[@class='topbarItem']/li[@role='menuitem']/div/span/span")
        exceloperator=Excel()
        exceloperator.create_excel_file(filename,sheetname)
        #tobarMenuNameList=[]
        row1=1
        row = 1
        col = 1
        app = xw.App(visible=True, add_book=False)
        wb = app.books.open(filename)

        for name in tobarMenuElement:
            tobarMenuName=name.text
            #tobarMenuNameList.append(tobarMenuName)
            wb.sheets[0].range("a"+str(row)).value = tobarMenuName
            name.click()
            self.waitloading()
            time.sleep(2)
            nestmenus=None
            nestmenus=self.get_elements("x","//div[@class='el-menu--horizontal' and not (contains(@style,'display: none;'))]//div[@class='nest-menu']/li[@role='menuitem'][@class='el-menu-item tos-menu-item']/a/span/span")
            for x in nestmenus:
                nestName=x.text
                #x.click()
                wb.sheets[sheetname].range("b" + str(row1)).value = nestName
                row1=row1+1
            row=row+1
            wb.save()
        wb.close()
        app.quit()
