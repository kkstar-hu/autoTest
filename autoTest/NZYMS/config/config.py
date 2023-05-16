from Commons.RandomFunction import CommonGenerator

host="http://10.126.0.89:7980/#/login"
#进场计划箱号
global boxNumber
boxNumber=CommonGenerator.generate_spec("JXNU",7)
# boxNumber="JXNU4000000"

global boxNumberOutPlan
# boxNumberOutPlan=CommonGenerator.generate_spec("CZXZ",7)
boxNumberOutPlan="CZXZ3016897"

global planNumber
#查询箱信息内容，字典模式
global dict
#出场计划号
global outplanNumber
#散货入库计划号
global bulkintoNumber
#散货出库计划号
global bulkoutNumber
#查验计划号
global checkplanNumber
#装箱计划号
global packingboxNumber
#拆箱计划好
global splitboxNumber
username='9541'
password="q11111111@"
showname="祁洲海"
createName="8541/祁洲海"