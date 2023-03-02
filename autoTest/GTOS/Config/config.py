from Commons.RandomFunction import CommonGenerator

host="http://10.166.0.155/app/#/login"

#驳船内容
#进场计划箱号
global boxNumber
boxNumber=CommonGenerator.generate_spec("XCXZ",7)
# boxNumber="XCXZ4981072"

#直提箱编号
global boxNumberTwo
boxNumberTwo=CommonGenerator.generate_spec("ZTXZ",7)
# boxNumberTwo ='ZTXZ7905421'

#直装箱编号
global boxNumberThree
boxNumberThree=CommonGenerator.generate_spec("ZZXZ",7)
# boxNumberThree ='ZZXZ3517204'


#闲置集卡号
global carnumber
#箱位置
global boxPosition
# boxPosition='A01079031'


global outBoxNumber
outBoxNumber=CommonGenerator.generate_spec("JXNU",7)
# outBoxNumber="JXNU4318659"


#航次随机数
voyage = CommonGenerator.generate_verify_code(4)
#进口航次
global importNumber
importNumber = 'I'+voyage
# importNumber="I8910"
# importNumber=CommonGenerator.generate_spec("I",4)

# 出口航次
global outportNumber
outportNumber = 'E'+voyage
# outportNumber="E8910"
# outportNumber=CommonGenerator.generate_spec("E",4)


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
showname="A"
createName="8541/祁洲海"