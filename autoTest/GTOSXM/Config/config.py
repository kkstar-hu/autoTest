from Commons.RandomFunction import CommonGenerator

host = "http://web.cloudtos-xm.com/#/login"   #β环境

#host = "http://web.cloudtos.com/#/login"   #α环境

# 驳船内容
global boxNumber
#boxNumber = CommonGenerator.generate_spec("XCTX", 7)   # 卸船提箱箱号
boxNumber="XCTX0317298"

global boxNumberTwo
#boxNumberTwo = CommonGenerator.generate_spec("ZTXZ", 7)  # 直提箱编号
boxNumberTwo ='ZTXZ0589473'

global boxNumberThree
#boxNumberThree = CommonGenerator.generate_spec("ZZXZ", 7)   # 直装箱编号
boxNumberThree ='ZZXZ5869137'

global carnumber  # 闲置集卡号
# carnumber='008'

global boxPosition   # 箱位置
boxPosition='B1049012'

global outBoxNumber
#outBoxNumber = CommonGenerator.generate_spec("JXZX", 7)    # 进箱、装箱流程
outBoxNumber="JXZX5716930"

voyage = CommonGenerator.generate_verify_code(4)    # 航次随机数

global importNumber
# importNumber = 'I'+voyage
# importNumber="I4627" #驳船
# importNumber="I4139" #大船
importNumber = "I7068"  # 空箱输运航次
# importNumber=CommonGenerator.generate_spec("I",4)

# 出口航次
global outportNumber
# outportNumber = 'E'+voyage
# outportNumber="E4627" #驳船
# outportNumber="E4139" #大船
omportNumber = "E7068"  # 空箱输运航次
# outportNumber=CommonGenerator.generate_spec("E",4)

# 提箱预约号
global Number


global takeNumber
takeNumber = CommonGenerator.generate_verify_code(4)  # 进箱提单号
# takeNumber='JXZX1362480'
# 登录信息

username = "admintst"    #β环境
password = "ctos@123"
showname = "XRCT"

# username = "admin"          #α环境
# password = "ctos@1234"
# showname = "XRCT"
