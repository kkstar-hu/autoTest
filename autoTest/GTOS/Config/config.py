from Commons.RandomFunction import CommonGenerator

host="http://10.166.0.155/app/#/login"

#驳船内容
#进场计划箱号
global boxNumber
boxNumber=CommonGenerator.generate_spec("JXNU",7)
# boxNumber="JXNU6875109"

#直提箱编号
global boxNumberTwo
boxNumberTwo=CommonGenerator.generate_spec("ZTXZ",7)
# boxNumberTwo ='JXNU1001'

#直装箱编号
global boxNumberThree
boxNumberThree=CommonGenerator.generate_spec("ZZXZ",7)
# boxNumberThree ='ZZXZ3517204'


#箱位置
global boxPosition
# boxPosition='A03011031'


global outBoxNumber
outBoxNumber="I107"

#进口航次
global importNumber
importNumber="I101"
#出口航次
global outportNumber
outportNumber="E101"

#提箱预约号
global Number


#大船内容
global bigshipimportNumber
global bigshipoutportNumber
bigshipimportNumber="I0001"
bigshipoutportNumber="1000E"


#登录信息
takeNumber="1014" #进箱提单号
username="admin"
password="ctos@12345"
showname="管理员"
createName="8541/祁洲海"