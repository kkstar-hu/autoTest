from Commons.RandomFunction import CommonGenerator

# host = "http://web.cloudtos-xm.com/#/login"   #β环境
host = "http://web.cloudtos.com/#/login"       #α环境

#登录账号
if 'xm' in host:
    username = "autotest"    #β环境
    password = "ctos@1234"
    showname = "XRCT"
else:
    username = "admin"       #α环境
    password = "ctos@1234"
    showname = "XRCT"

# 驳船内容
global boxNumber
boxNumber = CommonGenerator.generate_spec("XCTX", 7)   # 卸船提箱箱号
# boxNumber="XCTX4361278"

global boxNumberTwo
boxNumberTwo = CommonGenerator.generate_spec("ZTXZ", 7)  # 直提箱编号
# boxNumberTwo ='ZTXZ1670582'

global boxNumberThree
boxNumberThree = CommonGenerator.generate_spec("ZZXZ", 7)   # 直装箱编号
# boxNumberThree ='ZZXZ3754296'

global carnumber  # 闲置集卡号
# carnumber='052'

# global boxPosition   # 箱位置
# boxPosition='C1001101'

global outBoxNumber
outBoxNumber = CommonGenerator.generate_spec("JXZX", 7)    # 进箱、装箱流程
# outBoxNumber="JXZX2087395"

voyage = CommonGenerator.generate_verify_code(4)    # 航次随机数

global importNumber
# importNumber = 'I'+voyage
importNumber="I9145" #大船
#importNumber=CommonGenerator.generate_spec("I", 4)

# 出口航次
global outportNumber
# outportNumber = 'E'+voyage
outportNumber="E9145" #驳船
#outportNumber=CommonGenerator.generate_spec("E", 4)

# 提箱预约号
global Number


global takeNumber
takeNumber = CommonGenerator.generate_verify_code(4)  # 进箱提单号
# takeNumber='JXZX1362480'