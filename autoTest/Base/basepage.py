from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from Commons.log import getlogger
import pytest_check as check
import time

class BasePage:

    def __init__(self,driver):
        """
        运行初始化方法
        """
        self.driver = driver
        self.logger = getlogger()

    def get_element(self, selector_by, selector_value):
        """
        获取元素，通过，区分开，类别 内容
        ('x,//*[@id="kw"])
        """
        if selector_by == "i" or selector_by == "id":
            w_element = self.driver.find_element(By.ID, value=selector_value)
        elif selector_by == "x" or selector_by == "xpath":
            w_element = self.driver.find_element(By.XPATH, value=selector_value)
        elif selector_by == "n" or selector_by == "name":
            w_element = self.driver.find_element(By.NAME, value=selector_value)
        elif selector_by == "c" or selector_by == "class_name":
            w_element = self.driver.find_element(By.CLASS_NAME, value=selector_value)
        elif selector_by == "l" or selector_by == "link_text":
            w_element = self.driver.find_element(By.LINK_TEXT, value=selector_value)
        elif selector_by == "p" or selector_by == "partial_link":
            w_element = self.driver.find_element(By.PARTIAL_LINK_TEXT, value=selector_value)
        elif selector_by == "t" or selector_by == "tag_name":
            w_element = self.driver.find_element(By.TAG_NAME, value=selector_value)
        elif selector_by == "s" or selector_by == "css":
            w_element = self.driver.find_element(By.CSS_SELECTOR, value=selector_value)
        else:
            return None
        time.sleep(0.2)
        return w_element


    def get_elements(self, selector_by, selector_value):
        """
        获取元素列表，通过，区分开，类别 内容
        """
        if selector_by == "i" or selector_by == "id":
            elements = self.driver.find_elements(By.ID, value=selector_value)
        elif selector_by == "x" or selector_by == "xpath":
            elements = self.driver.find_elements(By.XPATH, value=selector_value)
        elif selector_by == "n" or selector_by == "name":
            elements = self.driver.find_elements(By.NAME, value=selector_value)
        elif selector_by == "c" or selector_by == "class_name":
            elements = self.driver.find_elements(By.CLASS_NAME, value=selector_value)
        elif selector_by == "l" or selector_by == "link_text":
            elements = self.driver.find_elements(By.LINK_TEXT, value=selector_value)
        elif selector_by == "p" or selector_by == "partial_link":
            elements = self.driver.find_elements(By.PARTIAL_LINK_TEXT, value=selector_value)
        elif selector_by == "t" or selector_by == "tag_name":
            elements = self.driver.find_elements(By.TAG_NAME, value=selector_value)
        elif selector_by == "s" or selector_by == "css":
            elements = self.driver.find_elements(By.CSS_SELECTOR, value=selector_value)
        else:
            return None
        time.sleep(0.2)
        return elements

    # 输入内容带清除
    def input(self, selector_by, selector_value, value):
        webelement = self.get_element(selector_by, selector_value)
        webelement.clear()
        webelement.send_keys(value)


    #当页面多个相同的控件用此方法
    def input_by_index(self, selector_by, selector_value, value,index=1):
        webelement = self.get_elements(selector_by, selector_value)[index]
        webelement.clear()
        webelement.send_keys(value)

    def input_no_clear(self, selector_by, selector_value, value):
        self.get_element(selector_by, selector_value).send_keys(value)

    def input_no_clear_index(self,selector_by, selector_value, value,index=1):
        em = self.get_elements(selector_by, selector_value)[index]
        em.send_keys(value)


    def click(self, by,selector):
        self.get_element(by,selector).click()

    # 当页面多个相同的控件用此方法
    def click_by_index(self, by, selector,index):
        self.get_elements(by, selector)[index].click()

    # 输入url地址访问网站
    def geturl(self, url, time=8):
        self.driver.get(url)
        self.driver.maximize_window()
        self.driver.implicitly_wait(time)

    def elementExist(self,by,selector):
        """
        判断元素是否存在
        """
        try:
            self.get_element(by,selector)
            return True
        except Exception as e:
            return False

    # 隐士等待
    def waitloading(self, seconds=3):
        self.driver.implicitly_wait(seconds)

    # 显示等待
    def element_wait(self, by, value, secs=5):
        """
        等待元素显示
        """
        try:
            if by == "id":
                WebDriverWait(self.driver, secs, 1).until(EC.presence_of_element_located((By.ID, value)))
            elif by == "name":
                WebDriverWait(self.driver, secs, 1).until(EC.presence_of_element_located((By.NAME, value)))
            elif by == "class":
                WebDriverWait(self.driver, secs, 1).until(EC.presence_of_element_located((By.CLASS_NAME, value)))
            elif by == "link_text":
                WebDriverWait(self.driver, secs, 1).until(EC.presence_of_element_located((By.LINK_TEXT, value)))
            elif by == "xpath":
                WebDriverWait(self.driver, secs, 1).until(EC.presence_of_element_located((By.XPATH, value)))
            elif by == "css":
                WebDriverWait(self.driver, secs, 1).until(EC.presence_of_element_located((By.CSS_SELECTOR, value)))
            else:
                raise NoSuchElementException(
                    "找不到元素，请检查语法或元素")
        except TimeoutException:
            print("查找元素超时请检查元素")

        # 显示等待
    def get_element_wait(self, by, value, secs=5):
        """
        等待元素显示
        """
        try:
            if by == "id":
                WebDriverWait(self.driver, secs, 1).until(EC.presence_of_element_located((By.ID, value)))
            elif by == "name":
                WebDriverWait(self.driver, secs, 1).until(EC.presence_of_element_located((By.NAME, value)))
            elif by == "class":
                WebDriverWait(self.driver, secs, 1).until(EC.presence_of_element_located((By.CLASS_NAME, value)))
            elif by == "link_text":
                WebDriverWait(self.driver, secs, 1).until(EC.presence_of_element_located((By.LINK_TEXT, value)))
            elif by == "xpath":
                WebDriverWait(self.driver, secs, 1).until(EC.presence_of_element_located((By.XPATH, value)))
            elif by == "css":
                WebDriverWait(self.driver, secs, 1).until(EC.presence_of_element_located((By.CSS_SELECTOR, value)))
            else:
                raise NoSuchElementException(
                    "找不到元素，请检查语法或元素")
        except TimeoutException:
            print("查找元素超时请检查元素")
        else:
            return self.get_element(by, value)

    def element_wait_disappear(self, by, value, secs=5):
        """
        等待元素消失
        """
        try:
            if by == "id":
                WebDriverWait(self.driver, secs, 1).until_not(EC.presence_of_element_located((By.ID, value)))
            elif by == "name":
                WebDriverWait(self.driver, secs, 1).until_not(EC.presence_of_element_located((By.NAME, value)))
            elif by == "class":
                WebDriverWait(self.driver, secs, 1).until_not(EC.presence_of_element_located((By.CLASS_NAME, value)))
            elif by == "link_text":
                WebDriverWait(self.driver, secs, 1).until_not(EC.presence_of_element_located((By.LINK_TEXT, value)))
            elif by == "xpath":
                WebDriverWait(self.driver, secs, 1).until_not(EC.presence_of_element_located((By.XPATH, value)))
            elif by == "css":
                WebDriverWait(self.driver, secs, 1).until_not(EC.presence_of_element_located((By.CSS_SELECTOR, value)))
            else:
                raise NoSuchElementException(
                    "找不到元素，请检查语法或元素")
        except TimeoutException:
            print("查找元素超时请检查元素")

    def refresh(self):
        """
        刷新当前页面
        """
        self.driver.refresh()

    def quite_driver(self):
        """
        退出浏览器
        """
        self.driver.quit()

    def close_current_page(self):
        """
        关闭当前窗口
        """
        self.driver.close()

    def scroll_to_view(self, selector):
        """
        滚动到元素
        """
        e1 = self.get_element("xpath",selector)
        self.driver.execute_script('arguments[0].scrollIntoView(false);', e1)

    def get_attribute_info(self,by,selector, attribute_kind):
        """
        获取元素的信息，
        """
        e1 = self.get_element(by,selector)
        r_a = e1.get_attribute(attribute_kind)
        return r_a

    def get_text(self,by,selector):
        """
        获得元素文本信息
        用法:
        driver.get_text("css=>#el")
        """
        el = self.get_element_wait(by,selector)
        return el.text


    def get_value(self,by,selector):
        """
        获得元素文本信息
        用法:
        driver.get_text("css=>#el")
        """
        return self.get_attribute_info(by,selector,'textContent')


    #从0开始
    def get_text_index(self,by,selector,index):
        el = self.get_elements(by,selector)[index]
        return  el.text

    def compareValue(self,by,selector, expect):
        actual = self.get_text(by,selector).strip()
        check.equal(actual,expect)

    def containValue(self,by,selector, expect):
        actual = self.get_text(by,selector).strip()
        check.is_in(actual,expect)

    def get_display(self,by,selector,index):
        """
        获取元素来显示，返回结果为真或假.
        用法:
        driver.get_display("css=>#el")
        """
        el = self.get_elements(by,selector)[index]
        return el.is_displayed()

    def get_enable(self,by,selector,index):
        """
        获取元素来显示，返回结果为真或假.
        用法:
        driver.get_display("css=>#el")
        """
        el = self.get_elements(by,selector)[index]
        return el.is_enabled()

    def get_title(self):
        """
        获取当前页面的title
        """
        return self.driver.title

    def get_current_url(self):
        """
        获取当前页面的url
        """
        return self.driver.current_url

    def switch_to_frame(self, selector):
        """
        嵌套的frame ，切换到指定iframe
        """
        e1 = self.get_element(selector)
        self.driver.switch_to.frame(e1)

    def switch_to_frame_by_handle(self, handle):
        """
        嵌套的frame ，通过handle
        """
        self.driver.switch_to.frame(handle)

    def switch_to_default_frame(self):
        """
        切换到默认的 frame
        """
        self.driver.switch_to.default_content()

    def switch_to_window(self, handle):
        """
        切换窗口，通过 handle
        """
        self.driver.switch_to.window(handle)


    def switchWindow(self, index):
        """
        切换窗口，通过index第几个窗口，从0开始
        """
        self.driver.switch_to.window(self.get_all_handles()[index])

    def get_all_handles(self):
        """
        获取所有串口的handles
        """
        all_handles = self.driver.window_handles
        return all_handles

    def get_current_handle(self):
        """
        获取当前页面的handle
        """
        return self.driver.current_window_handle

    def switch_to_new_close_other(self, target_handle):
        """
        关闭当前页面的其他页面
        """
        all_handles = self.driver.window_handles
        if target_handle in all_handles:
            for one_h in all_handles:
                if one_h != target_handle:
                    self.switch_to_window(one_h)
                    self.close_brower()
                    self.switch_to_window(target_handle)

    def get_alert_text(self):
        """
        获取提示信息
        """
        try:
            return self.get_text("xpath","//div[@role='alert']//p")
        except:
            self.logger.error("未发现提示信息")


    #判断是否存在提示信息
    def has_alert(self,expectAlert):
        """
        获取提示信息
        """
        return self.elementExist("xpath",f"//div[@role='alert']//p[contains(text(),'{expectAlert}')]")

    def check_alert(self, expectAlert):
        try:
            check.equal(self.get_alert_text(),expectAlert)
        except:
            pass

    def check_alert_and_close(self, expectAlert):
        check.equal(self.get_alert_text(), expectAlert)
        try:
            self.click('xpath',f"//div[@role='alert']//p[text()='{expectAlert}']/following::div[@class='el-notification__closeBtn el-icon-close']")
        except:
            self.click('xpath',f"//div[@class='el-notification__closeBtn el-icon-close']")

    def close_alert(self,name):
        """
        关闭提示信息
        """
        self.click('xpath', f"//div/p[text()='{name}']/following::div[@class='el-notification__closeBtn el-icon-close']")



    def wait_element_appear(self, selector, wait_time=10):
        """
        等待元素出现
        """
        time.sleep(1)
        flag = True
        while self.element_exist(selector):
            time.sleep(1)
            wait_time -= 1
            if wait_time == 0:
                flag = False
                break
        return flag

    def right_click(self,by,selector):
        """
        鼠标右键点击
        """
        e1 = self.get_element(by,selector)
        ActionChains(self.driver).context_click(e1).perform()

    def left_click(self,by,selector):
        """
        鼠标左键点击
        """
        e1 = self.get_element(by,selector)
        ActionChains(self.driver).click(e1).perform()

    def double_click(self, by,selector):
        """
        双击元素.
        用法:
        driver.double_click("css=>#el")
        """
        el = self.get_element(by,selector)
        ActionChains(self.driver).double_click(el).perform()

    def move_mouse_to_element(self,by, selector):
        """
        鼠标移动元素上，悬浮
        """
        e1 = self.get_element(by,selector)
        ActionChains(self.driver).move_to_element(e1).perform()


    def drag_mouse_to_element(self,by1,source,by2,target):
        """
        鼠标拖动元素
        """
        e1 = self.get_element(by1,source)
        e2 = self.get_element(by2,target)
        ActionChains(self.driver).drag_and_drop(e1, e2).perform()

    def clickandhold(self, selector):
        """
        鼠标左键按住不放
        """
        ActionChains(self.driver).click_and_hold(selector).perform()

    def move_by_xy(self, offsetx, offsety):
        """
        移动到某个坐标上
        """
        ActionChains(self.driver).move_by_offset(offsetx, offsety).perform()

    def move_release(self):
        ActionChains(self.driver).release().perform()

    def get_page_source(self):
        """
        获取当前页面的source
        """
        html_txt = self.driver.page_source
        return html_txt

    def get_default_select_value(self, selector):
        e1 = Select(self.get_element(selector)).first_selected_option
        select_text = e1.get_attribute('text')
        return select_text

    def get_select_values(self, selector):
        """
        获取下拉框的全部值
        """
        name_list = []
        e1_all = Select(self.get_element(selector)).options
        for e1 in e1_all:
            select_txt = e1.get_attribute("text")
            name_list.append(select_txt)
        return name_list

    def hasInput(self,input,data):
        try:
            input[data]
        except KeyError:
            return False
        else:
            return True
    def take_screen_shot(self, file_name):
        """
        page 页面截图操作
        """
        self.driver.save_screenshot(file_name)

    def js(self, script):
        """
        执行JavaScript脚本.
        用法:
        driver.js("window.scrollTo(200,1000);")
        """
        self.driver.execute_script(script)

    #点击保存并关闭按钮
    def save_and_close(self):
        self.click("xpath","//button/span[contains(text(),'保存并关闭')]")
        self.waitloading()


    # 点击保存并关闭按钮
    def save(self):
        self.click("xpath", "//button/span[contains(text(),'保 存')]")
        self.waitloading()

        # 点击保存并关闭按钮

    def cancel(self):
        self.click("xpath", "//button//span[text()='取消']")
        self.waitloading()

     #关闭窗口X
    def close(self):
        self.click('xpath','//i[@class="el-dialog__close el-icon el-icon-close"]')
        self.waitloading()
