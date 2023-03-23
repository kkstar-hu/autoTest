from Commons.RandomFunction import CommonGenerator

host="http://web.cloudtos.com/#/login"

#驳船内容
#卸船提箱箱号
global boxNumber
boxNumber=CommonGenerator.generate_spec("XCTX",7)
# boxNumber="XCTX8024136"

#直提箱编号
global boxNumberTwo
boxNumberTwo=CommonGenerator.generate_spec("ZTXZ",7)
# boxNumberTwo ='ZTXZ1629045'

#直装箱编号
global boxNumberThree
boxNumberThree=CommonGenerator.generate_spec("ZZXZ",7)
# boxNumberThree ='ZZXZ2137456'

#闲置集卡号
global carnumber

#箱位置
global boxPosition
# boxPosition='T6001011'

#进箱、装箱流程
global outBoxNumber
outBoxNumber=CommonGenerator.generate_spec("JXZX",7)
# outBoxNumber="JXZX5142096"

#航次随机数
voyage = CommonGenerator.generate_verify_code(4)
#进口航次
global importNumber
importNumber = 'I'+voyage
#importNumber="I9284"
#importNumber=CommonGenerator.generate_spec("I",4)

# 出口航次
global outportNumber
outportNumber = 'E'+voyage
#outportNumber="E4280"
#outportNumber=CommonGenerator.generate_spec("E",4)


#提箱预约号
global Number


#大船内容
global bigshipimportNumber
global bigshipoutportNumber
bigshipimportNumber="I0001"
bigshipoutportNumber="1000E"

global takeNumber
takeNumber=CommonGenerator.generate_verify_code(4) #进箱提单号
# takeNumber='JXZX1362480'
#登录信息

username="admin"
password="ctos@12345"
showname="XRCT"