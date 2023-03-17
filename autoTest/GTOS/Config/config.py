from Commons.RandomFunction import CommonGenerator

host="http://10.166.0.155/app/#/login"

#驳船内容
#进场计划箱号
global boxNumber
boxNumber=CommonGenerator.generate_spec("XCXZ",7)
# boxNumber="XCXZ7043981"

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
# boxPosition='A01013093'


global outBoxNumber
outBoxNumber=CommonGenerator.generate_spec("JXNU",7)
# outBoxNumber="JXNU0124369"


#航次随机数
voyage = CommonGenerator.generate_verify_code(4)
#进口航次
global importNumber
# importNumber = 'I'+voyage
# 驳船
# importNumber="I1309"
#大船
importNumber="I1309"
# importNumber=CommonGenerator.generate_spec("I",4)

# 出口航次
global outportNumber
# outportNumber = 'E'+voyage
#驳船
# outportNumber="E2347"
#大船
outportNumber="E1309"
# outportNumber=CommonGenerator.generate_spec("E",4)


#提箱预约号
global Number


#大船内容
global bigshipimportNumber
global bigshipoutportNumber
bigshipimportNumber ='I'+voyage
# bigshipimportNumber = 'I1309'
bigshipoutportNumber ='E'+voyage
# bigshipoutportNumber = 'E1309'


#登录信息
takeNumber="1014" #进箱提单号
username="admin"
password="ctos@12345"
showname="A"
createName="8541/祁洲海"