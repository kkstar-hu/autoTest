# -*- coding:utf-8 -*-
from BTOSLJ.Controls.BTOS_data import BtosTempData, BtosCustomData
from Commons.RandomFunction import CommonGenerator

host = "http://10.166.0.131:20000/#/login"

request_blj_host = "10.116.8.16:8520"

# 账户
username = "ljadmin"
password = "q1234567"
showname = "罗泾管理员"

global mydata
mydata = BtosTempData()
# 船舶资料
mydata.vsl_cd = "AUTO TEST"
mydata.vsl_cnname = "测试船舶"
mydata.vsl_enname = "AUTO TEST"
mydata.vsl_loa = 150
mydata.hatchamount = 10
global importNumber
#importNumber=CommonGenerator.generate_spec("I",4)
importNumber="B0313J"
global outportNumber
#outportNumber=CommonGenerator.generate_spec("E",4)
outportNumber=None

# 其他数据
c = BtosCustomData()
mydata.gtypecd, mydata.pktype = c.get_pktype
mydata.licese_plate = c.get_license_plate
mydata.bill = c.get_bill
mydata.voyage = c.get_Ivoyage
#mydata.print_data