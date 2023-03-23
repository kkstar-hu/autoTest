from Commons.RandomFunction import CommonGenerator

host="http://web.cloudtos.com/#/login"

#驳船内容
#卸船提箱箱号
global boxNumber
boxNumber=CommonGenerator.generate_spec("XCTX",7)
# boxNumber="XCTX2031867"

#直提箱编号
global boxNumberTwo
boxNumberTwo=CommonGenerator.generate_spec("ZTXZ",7)
# boxNumberTwo ='ZTXZ6409318'

#直装箱编号
global boxNumberThree
boxNumberThree=CommonGenerator.generate_spec("ZZXZ",7)
# boxNumberThree ='ZZXZ4167903'

#闲置集卡号
global carnumber

#箱位置
global boxPosition
# boxPosition='C1055011'

#进箱、装箱流程
global outBoxNumber
outBoxNumber=CommonGenerator.generate_spec("JXZX",7)
# outBoxNumber="JXZX9508631"

#航次随机数
voyage = CommonGenerator.generate_verify_code(4)
#进口航次
global importNumber
importNumber = 'I'+voyage
#驳船
# importNumber="I7068"
#大船
# importNumber="I6241"
# importNumber=CommonGenerator.generate_spec("I",4)

# 出口航次
global outportNumber
outportNumber = 'E'+voyage
#驳船
# outportNumber="E7068"
#大船
# outportNumber="E6241"
# outportNumber=CommonGenerator.generate_spec("E",4)


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