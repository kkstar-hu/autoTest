from Commons.RandomFunction import CommonGenerator

host="http://10.166.0.155/app/#/login"

#驳船内容
#卸船提箱箱号
global boxNumber
boxNumber=CommonGenerator.generate_spec("XCTX",7)
#boxNumber="JXNU1000005"

#直提箱编号
global boxNumberTwo
boxNumberTwo=CommonGenerator.generate_spec("ZTXZ",7)
#boxNumberTwo ='ZTXZ1000020'

#直装箱编号
global boxNumberThree
boxNumberThree=CommonGenerator.generate_spec("ZZXZ",7)
#boxNumberThree ='ZZXZ1000021'


#箱位置
global boxPosition
# boxPosition='A03011031'

#进箱、装箱流程
global outBoxNumber
outBoxNumber=CommonGenerator.generate_spec("JXZX",7)
#outBoxNumber="JXNU1000017"

#进口航次
global importNumber
importNumber=CommonGenerator.generate_spec("I",3)
#importNumber="I311"
#出口航次
global outportNumber
outportNumber=CommonGenerator.generate_spec("E",3)
#outportNumber="E311"

#提箱预约号
global Number


#大船内容
global bigshipimportNumber
global bigshipoutportNumber
bigshipimportNumber="I0001"
bigshipoutportNumber="1000E"

global takeNumber
takeNumber=CommonGenerator.generate_verify_code(4) #进箱提单号
#登录信息

username="admin"
password="ctos@12345"
showname="管理员"