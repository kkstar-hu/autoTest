# -*- coding:utf-8 -*-

import base64
import time

import cv2
from Base.basepage import BasePage
from selenium import webdriver
from BTOSLJ.Config import config

class Login(BasePage):
    def login(self):
        self.driver.get(config.host)
        self.input_by_index("x", "//input[@name='useraccount']", config.username, 1)
        self.input_by_index("x", "//input[@name='password']", config.password, 1)
        self.click("x", "//div[@id='app']/div[3]//span[contains(text(),'登录')]/..")
        #k = 1
        # 获取原图
        bg_img = self.get_element_wait("xpath","//div[@class='verify-img-panel']/img", 1)
        background_url = bg_img.get_attribute("src")
        self.onload_save_img(background_url[22:], '../../../img/background.png')
        # 获取缺块
        front_img = self.get_element_wait("xpath","//div[@class='verify-sub-block']/img", 1)
        slider_url = front_img.get_attribute("src")  # 获取图片地址
        self.onload_save_img(slider_url[22:], '../../../img/slider.png') # 保存图片
        # 获取滑块
        slide_element = self.get_element_wait("xpath","//div[@class='verify-move-block']", 1)
        distance = self.identify_gap() + 12  # 滑动距离
        self.clickandhold(slide_element)  # 长按滑块
        self.move_by_xy(distance, 0)  # 拖动滑块
        self.move_release()  # 松开滑块
        # yz = self.get_element.("xpath", "//div[@class='verify-img-panel']/span").text
        # if(yz != "验证失败"):
        #     break

    def onload_save_img(self,url,filename):
        img = base64.b64decode(url)  #base64转图片
        file = open(filename,'wb')
        file.write(img)
        file.close()


    '''计算滑动距离'''
    def identify_gap(self,out = "../../../img/out.png"):

        # 读取背景图片和缺口图片
        bg_img = cv2.imread("../../../img/background.png") # 背景图片
        tp_img = cv2.imread("../../../img/slider.png") # 缺口图片

        # 边缘检测
        bg_edge = cv2.Canny(bg_img, 100, 200)
        tp_edge = cv2.Canny(tp_img, 100, 200)

        bg_pic = cv2.cvtColor(bg_edge, cv2.COLOR_GRAY2RGB)
        tp_pic = cv2.cvtColor(tp_edge, cv2.COLOR_GRAY2RGB)

        # 最佳匹配
        res = cv2.matchTemplate(bg_pic, tp_pic, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        # 绘制方框
        th, tw = tp_pic.shape[:2]
        tl = max_loc  # 左上角坐标
        br = (tl[0]+tw,tl[1]+th) # 右下角坐标
        cv2.rectangle(bg_img, tl, br, (0, 0, 255), 2) # 绘制矩形
        cv2.imwrite(out, bg_img)
        # 返回缺口的 x 坐标
        return tl[0]
