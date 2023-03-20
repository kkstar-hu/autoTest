from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from Base.basepage import BasePage
from Commons.utils import get_distance
import base64
import time

class Login(BasePage):

    def login(self,username,password,showName):
        self.logger.info('步骤1输入用户名')
        if username!=None:
            self.get_elements("xpath","//input[@placeholder='请输入用户名']")[1].send_keys(username)
        self.logger.info('步骤2输入密码')
        if password!= None:
            self.get_elements("xpath","//input[@placeholder='请输入密码']")[1].send_keys(password)
        self.get_elements("xpath", "//button[@class='el-button login-btn el-button--primary el-button--bg']")[1].click()
        self.waitloading()
        self.drogImage(self.driver)
        self.element_wait("xpath","//div[@role='alert']//p")
        self.compareValue("xpath","//div[@class='avatar-wrapper el-dropdown-selfdefine']//span",showName)

    def drogImage(self,driver):
        try:
            JS1 = 'return document.querySelector("body > div.vue-puzzle-vcode.show_ > div > div.auth-body_ > canvas:nth-child(1)").toDataURL("image/jpeg");'
            JS2 = 'return document.querySelector("body > div.vue-puzzle-vcode.show_ > div > div.auth-body_ > canvas.auth-canvas2_").toDataURL("image/jpeg");'

            k = 0
            while k < 60:
                time.sleep(2)
                canvas1 = driver.execute_script(JS1)
                im_base641 = canvas1.split(',')[1]
                img1 = base64.b64decode(im_base641)
                with open('1.png', 'wb') as f:
                    f.write(img1)

                canvas2 = self.driver.execute_script(JS2)
                im_base642 = canvas2.split(',')[1]
                img2 = base64.b64decode(im_base642)
                with open('2.png', 'wb') as f:
                    f.write(img2)

                distance = get_distance() + 10  # 滑动距离
                self.clickandhold("xpath","/html/body/div[2]/div/div[2]/div/div[2]")
                self.move_by_xy(distance, 0)
                self.move_release()  # 松开滑块
                info = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/div[1]/div[2]"))).text
                print(info)
                if (info == "验证通过！"):
                    break
                k = k + 1
        except:
            pass


