from Commons.RandomFunction import CommonGenerator

host="http://10.126.0.89:7980/#/login"
#进场计划箱号
global boxNumber
boxNumber=CommonGenerator.generate_spec("JXNU",7)
#boxNumber="JXNU7489305"

global boxNumberOutPlan
boxNumberOutPlan=CommonGenerator.generate_spec("JXNU",7)
#boxNumberOutPlan="JXNU7489305"

global planNumber
#查询箱信息内容，字典模式
global dict
#出场计划号
global outplanNumber
#散货入库计划号
global bulkintoNumber
#bulkintoNumber='WIP23030200011'
#散货出库计划号
global bulkoutNumber
#查验计划号
global checkplanNumber
#装箱计划号
global packingboxNumber
#拆箱计划好
global splitboxNumber
username=9540
password="861310Aa"
showname="胡康莉"
createName="8540/胡康莉"