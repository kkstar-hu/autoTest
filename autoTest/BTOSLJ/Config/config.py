# -*- coding:utf-8 -*-
from BTOSLJ.Controls.BTOS_data import BTOS_TempData, BTOS_CustomData

host = "http://10.166.0.131:20000/#/login"

# 账户
username = "ljadmin"
password = "q1234567"
showname = "罗泾管理员"

global mydata
mydata = BTOS_TempData()
# 船舶资料
mydata.vsl_cd = "AUTO TEST"
mydata.vsl_cnname = "测试船舶"
mydata.vsl_enname = "AUTO TEST"
mydata.vsl_loa = 150
mydata.hatchamount = 10

# 其他数据
c = BTOS_CustomData()
mydata.gtypecd, mydata.pktype = c.get_pktype
mydata.licese_plate = c.get_license_plate
mydata.bill = c.get_bill
mydata.voyage = c.get_Ivoyage
mydata.print_data