from Commons.RandomFunction import CommonGenerator

host="http://10.166.0.155/app/#/login"
#进场计划箱号
global boxNumber
#boxNumber=CommonGenerator.generate_spec("JXNU",7)
boxNumber="JXNU100"

#直提流程
global boxNumberTwo
#boxNumberTwo=CommonGenerator.generate_spec("ZTXZ",7)
boxNumberTwo ='JXNU1010'

global boxNumberThree
#boxNumberThree=CommonGenerator.generate_spec("ZZXZ",7)
boxNumberThree ='JXNU1011'

#进箱、装箱流程
global outBoxNumber
outBoxNumber="JXNU1009"

#进口航次
#importNumber=CommonGenerator.generate_spec("I",4)
global importNumber
importNumber="I107"
#出口航次
#outportNumber=CommonGenerator.generate_spec("I",4)
global outportNumber
outportNumber="E107"

global bigshipimportNumber
global bigshipoutportNumber
bigshipimportNumber="I0001"
bigshipoutportNumber="1000E"
#提箱预约号
global Number

username="admin"
password="ctos@12345"
showname="管理员"
createName="8541/祁洲海"

global takeNumber
takeNumber=CommonGenerator.generate_spec("TD", 4)