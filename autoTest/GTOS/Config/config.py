from Commons.RandomFunction import CommonGenerator

host="http://10.166.0.155/app/#/login"
#进场计划箱号
global boxNumber
boxNumber=CommonGenerator.generate_spec("JXNU",7)
# boxNumber="JXNU2356708"

global boxNumberTwo
boxNumberTwo=CommonGenerator.generate_spec("ZTXZ",7)
# boxNumberTwo ='JXNU2356708'

global boxNumberThree
boxNumberThree=CommonGenerator.generate_spec("ZZXZ",7)
# boxNumberThree ='ZZXZ1683790'
#进口航次
global importNumber
importNumber="I123"
#出口航次
global outportNumber
outportNumber="E123"

global bigshipimportNumber
global bigshipoutportNumber
bigshipimportNumber="I0001"
bigshipoutportNumber="1000E"
#提箱预约号
global Number
#船舶名称
# global shipname
# shipname = 'AQZ'
#箱位置
global boxPosition
# boxPosition = 'A01003091'
takeNumber="1014" #进箱提单号
username="admin"
password="ctos@12345"
showname="管理员"
createName="8541/祁洲海"