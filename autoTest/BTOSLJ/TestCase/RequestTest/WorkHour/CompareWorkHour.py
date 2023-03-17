# encoding = utf-8
from BTOSLJ.Controls.log import Log
from decimal import Decimal
import requests
import random
import re

# 计算结果
class result:
    def __init__(self, normHour:str, complemenHour:str, realHour:str):
        self.normHour = Decimal(normHour)
        self.complemenHour = Decimal(complemenHour)
        self.realHour = Decimal(realHour)
    def __eq__(self, other):
        if abs(self.normHour - other.normHour) <= 0.01 and abs(self.complemenHour - other.complemenHour) <= 0.01 and \
                abs(self.realHour - other.realHour) <= 0.02:
            return True
        return False
    def read(self):
        return [float(self.normHour), float(self.complemenHour), float(self.realHour)]

class WorkHour:
    def __init__(self):
        self.logger = Log().logger
        self.gtpks = random.randint(0,9999)   # 件数
        self.gtwg = round(random.uniform(0,9999),2)   # 吨位
        self.work_hour = round(random.uniform(0,30),2)  # 工作时间
        self.woker_complemen = random.randint(0,20)  # 加人
        self.woker_num = random.randint(0,50) # 计时工人数
        self.adjust_factor = round(random.uniform(0,5),2)  # 调节系数
        self.factor = round(random.uniform(0,5),2)  # 系数
        self.overtime_rate = round(random.uniform(0,5),2)  # 加班率
        self.plus_minus_hour = round(random.uniform(-10,10),2)  # 加减工时
        self.percentage = round(random.uniform(0,2),2)  # 百分比
        self.time_quota = None  # 工时定额
        self.hatch_hour = None  # 舱时量
        self.url_wsw = "http://10.166.0.131:20000/tos/pws/workSheetWk/real/manhour"
        self.url_wsm = "http://10.166.0.131:20000/tos/pws/workSheetMachine/real/manhour"
        self.url_quo = "http://10.166.0.131:20000/tos/pws/quota/"
        self.url_token = "http://10.166.0.131:20000/auth/saas/authorization/login/simple"
        self.piece_quoId = "94480e83378ebdc69f330703f5401457"
        self.weight_quoId = "93c05208559287f57c51817fb507a822"
        self.hour_quoId = "36cda28b65a59adda3586c9cdb495c4a"
        self.wswId = "26c977f42f7e6fa796afec9400d81ce4"
        self.wsmId = "50c4e3a9d0f9cf100b02c42b0b798aaf"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": None
        }
        self.pass_num = {
            "wsw_piece" : 0,
            "wsw_weight" : 0,
            "wsw_hour" : 0,
            "wsm_piece" : 0,
            "wsm_weight" : 0,
            "wsm_hour" : 0,
        }

    def get_token(self):
        payload = {
            "little_girl": "ljadmin",
            "little_boy": "q1234567",
            "verification": "xxx"
        }
        try:
            r = requests.post(url= self.url_token, json = payload)
            r.raise_for_status()
        except (requests.RequestException,requests.HTTPError) as e:
            self.logger.info(e)
        else:
            res = r.json()["data"]
            self.headers["Authorization"] = "Bearer " + res["access_token"]
        return 0


    # 获取工时定额、舱时量
    def get_quota(self, quo_id : str):
        try:
            r = requests.get(url= self.url_quo + quo_id, headers= self.headers)
            r.raise_for_status()
        except (requests.RequestException,requests.HTTPError) as e:
            self.logger.info(e)
        else:
            res = r.json()["data"]
            self.time_quota = res["quoTimeQuota"]
            self.hatch_hour = res["quoHatchHour"]
        return 0


    def generate(self):
        self.gtpks = random.randint(0,9999)   # 件数
        self.gtwg = round(random.uniform(0,9999),2)   # 吨位
        self.work_hour = round(random.uniform(0,30),2)  # 工作时间
        self.woker_complemen = random.randint(0,20)  # 加人
        self.woker_num = random.randint(0,50) # 计时工人数
        self.adjust_factor = round(random.uniform(0,5),2)  # 调节系数
        self.factor = round(random.uniform(0,5),2)  # 系数
        self.overtime_rate = round(random.uniform(0,5),2)  # 加班率
        self.plus_minus_hour = round(random.uniform(-10,10),2)  # 加减工时
        self.percentage = round(random.uniform(0,2),2)  # 百分比

    def compute(self, w : str, up_type : str):
        if(w == "wsw"):
            if(up_type == "piece"):
                normHour = Decimal(str(self.gtpks)) * Decimal(str(self.time_quota))
                complemenHour = Decimal(str(self.gtpks)) * Decimal(str(self.woker_complemen)) / Decimal(str(self.hatch_hour))
            elif(up_type == "weight"):
                normHour = Decimal(str(self.gtwg)) * Decimal(str(self.time_quota))
                complemenHour = Decimal(str(self.gtwg)) * Decimal(str(self.woker_complemen)) / Decimal(str(self.hatch_hour))
            elif(up_type == "hour"):
                normHour = Decimal(str(self.work_hour)) * Decimal(str(self.woker_num)) * Decimal(str(self.time_quota))
                complemenHour = Decimal(str(self.work_hour)) * Decimal(str(self.woker_num)) * \
                    Decimal(str(self.woker_complemen)) / Decimal(str(self.hatch_hour))

            realHour = (normHour + complemenHour) * Decimal(str(self.adjust_factor)) * Decimal(str(self.overtime_rate))\
                        + Decimal(str(self.plus_minus_hour))
            return self.save2(normHour), self.save2(complemenHour), self.save2(realHour)

        elif(w == "wsm"):
            if(up_type == "piece"):
                normHour = Decimal(str(self.gtpks)) / Decimal(str(self.hatch_hour))
            elif(up_type == "weight"):
                normHour = Decimal(str(self.gtwg)) / Decimal(str(self.hatch_hour))
            elif(up_type == "hour"):
                normHour = Decimal(str(self.work_hour)) * Decimal(str(self.time_quota))

            realHour = normHour * Decimal(str(self.adjust_factor)) * Decimal(str(self.factor)) * Decimal(str(self.percentage))\
                  * Decimal(str(self.overtime_rate)) + Decimal(str(self.plus_minus_hour))
            return self.save2(normHour), "0", self.save2(realHour)
        return 0

    def save2(self, num : Decimal):
        num = "%.50f"%(num)
        return re.findall(r"^-?\d{1,}?\.\d{2}", str(num))[0]

    def payload_wsw(self, wswQuoId : str):
        payload = {
            "wswId": self.wswId,
            "wswGtpks": self.gtpks,
            "wswGtwg": self.gtwg,
            "wswOvertimeRate": self.overtime_rate,
            "wswOvertimeTag": "N",
            "wswSupplyStandard": 0,
            "wswSupplyWeight": 0,
            "wswPlusMinusRate": 0,
            "wswQuoId": wswQuoId,
            "wswQuotano": "",
            "wswAdjustFactor": self.adjust_factor,
            "wswPlusMinusItem": 0,
            "wswWorkerComplemen": self.woker_complemen,
            "wswPlusMinusHour": self.plus_minus_hour,
            "wswWorkNum": self.woker_num,
            "wswWorkHour": self.work_hour
        }
        return payload

    def payload_wsm(self, wsmQuoId : str):
        payload = {
            "wsmId": self.wsmId,
            "wsmQuoId": wsmQuoId,
            "wsmQuotano": "",
            "wsmGtpks": self.gtpks,
            "wsmGtwg": self.gtwg,
            "wsmPlusMinusHour": self.plus_minus_hour,
            "wsmMealsHour": 0,
            "wsmFreeHour": 0,
            "wsmWorkHour": self.work_hour,
            "wsmPlusMinusRate": 0,
            "wsmPlusMinusItem": 0,
            "wsmOvertimeTag": "N",
            "wsmOvertimeRate": self.overtime_rate,
            "wsmAdjustFactor": self.adjust_factor,
            "wsmPercentage": self.percentage,
            "wsmFactor": self.factor
        }
        return payload

    def compare(self, w : str, up_type : str) :
        try:
            if(w == "wsw"):  # 装卸队
                if(up_type == "piece"):  # 计件
                    try:
                        r = requests.post(url= self.url_wsw, json= self.payload_wsw(self.piece_quoId),
                                            headers= self.headers)
                        r.raise_for_status()
                    except (requests.RequestException,requests.HTTPError) as e:
                        self.logger.info(e)
                    else:
                        res = r.json()["data"]
                        set2 = result(*self.compute(w = "wsw", up_type = "piece"))
                elif(up_type == "weight"):  # 计数
                    try:
                        r = requests.post(url= self.url_wsw, json= self.payload_wsw(self.weight_quoId),
                                            headers= self.headers)
                        r.raise_for_status()
                    except (requests.RequestException,requests.HTTPError) as e:
                        self.logger.info(e)
                    else:
                        res = r.json()["data"]
                        set2 = result(*self.compute(w = "wsw", up_type = "weight"))
                elif(up_type == "hour"):  # 计时
                    try:
                        r = requests.post(url= self.url_wsw, json= self.payload_wsw(self.hour_quoId),
                                            headers= self.headers)
                        r.raise_for_status()
                    except (requests.RequestException,requests.HTTPError) as e:
                        self.logger.info(e)
                    else:
                        res = r.json()["data"]
                        set2 = result(*self.compute(w = "wsw", up_type = "hour"))
                set1 = result(str(res["normHour"]),str(res["complemenHour"]),str(res["realHour"]))

            if(w == "wsm"):  # 员工
                if(up_type == "piece"):  # 计件
                    try:
                        r = requests.post(url= self.url_wsm, json= self.payload_wsm(self.piece_quoId),
                                            headers= self.headers)
                        r.raise_for_status()
                    except (requests.RequestException,requests.HTTPError) as e:
                        self.logger.info(e)
                    else:
                        res = r.json()["data"]
                        set2 = result(*self.compute(w = "wsm", up_type = "piece"))
                elif(up_type == "weight"):  # 计数
                    try:
                        r = requests.post(url= self.url_wsm, json= self.payload_wsm(self.weight_quoId),
                                            headers= self.headers)
                        r.raise_for_status()
                    except (requests.RequestException,requests.HTTPError) as e:
                        self.logger.info(e)
                    else:
                        res = r.json()["data"]
                        set2 = result(*self.compute(w = "wsm", up_type = "weight"))
                elif(up_type == "hour"):  # 计时
                    try:
                        r = requests.post(url= self.url_wsm, json= self.payload_wsm(self.hour_quoId),
                                            headers= self.headers)
                        r.raise_for_status()
                    except (requests.RequestException,requests.HTTPError) as e:
                        self.logger.info(e)
                    else:
                        res = r.json()["data"]
                        set2 = result(*self.compute(w = "wsm", up_type = "hour"))
                set1 = result(str(res["normHour"]), "0", str(res["realHour"]))
            right = True if set1 == set2 else False
            if(right):
                self.pass_num[w + "_" + up_type] = self.pass_num[w + "_" + up_type] + 1
            out = "" if set1 == set2 else (set1.read(), set2.read(),
                                           "请求参数: 件数 " + str(self.gtpks) + ",吨位 " + str(self.gtwg) + ",工作时间 " + str(self.work_hour)
                                           + ",加人 " + str(self.woker_complemen) + ",计时工人数 " + str(self.woker_num) + ",调节系数 " + str(self.adjust_factor)
                                           + ",系数 " + str(self.factor) + ",加班率 " + str(self.overtime_rate) + ",加减工时 " + str(self.plus_minus_hour)
                                           + ",百分比 " + str(self.percentage) + ",工时定额 " + str(self.time_quota) + ",舱时量 " + str(self.hatch_hour))
            self.logger.info("%s_%-6s : %s %s", w, up_type, right, out)
        except:
            pass

    def batch_run(self, n : int):
        num = n
        self.get_token()
        while n:
            self.get_quota(self.piece_quoId)
            self.compare("wsw","piece")
            self.compare("wsm","piece")
            self.get_quota(self.weight_quoId)
            self.compare("wsw","weight")
            self.compare("wsm","weight")
            self.get_quota(self.hour_quoId)
            self.compare("wsw","hour")
            self.compare("wsm","hour")
            n = n - 1
            self.generate()
        for k, v in zip(self.pass_num.keys(), self.pass_num.values()):
            self.logger.info("通过率 %-10s : %.2f%s", k, v/num*100, "%")
        self.logger.info("batch_num: %d", num)

if __name__ == '__main__':
    item = WorkHour()
    item.batch_run(100)