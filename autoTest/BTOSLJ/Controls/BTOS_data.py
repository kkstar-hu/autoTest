# -*- coding:utf-8 -*-
import random
import string
import time
from decimal import Decimal


class BTOS_TempData(object):
    def __init__(self):
        pass

    # 获取属性
    def __getattribute__(self, item):
        return object.__getattribute__(self, item)

    # 定义属性
    def __setattr__(self, item, value):
        object.__setattr__(self, item, value)

    @property
    def print_data(self):
        print(vars(self))


class BTOS_CustomData(object):
    def __init__(self):
        self.pktype = self.dict_pktype()
        self.billno = 1

    @staticmethod
    def dict_pktype():
        d = dict()
        d["钢板"] = "块"
        d["交通运输设备"] = "辆"
        d["卷钢"] = "卷"
        d["螺纹钢"] = "捆"
        d["开平板"] = "捆"
        d["纸浆(木浆)"] = "包"
        d["钢管"] = "捆"
        d["盘圆"] = "卷"
        d["圆钢"] = "支"
        d["钢坯"] = "块"
        d["冷卷"] = "卷"
        d["焦炭"] = "块"
        d["车辆"] = "辆"
        return d

    # 根据货名获取包装
    @property
    def get_pktype(self):
        gtypecd = random.choice(list(self.pktype.keys()))
        return gtypecd, self.pktype.get(gtypecd)

    # 航次
    @property
    def get_Ivoyage(iefg : str):
        return "B" + time.strftime('%m%d', time.localtime(time.time())) + "I"

    def get_Evoyage(iefg : str):
        return "B" + time.strftime('%m%d', time.localtime(time.time())) + "E"

    # 车牌号
    @property
    def get_license_plate(self):
        q1 = "鲁京津沪浙苏冀豫辽吉黑渝蒙桂宁藏新港澳赣皖闵粤贵云鄂湘川琼晋陕甘青台"
        return '{}{}'.format(random.choice(q1) + random.choice(string.ascii_uppercase),
                             "".join(random.sample([x for x in string.digits + string.ascii_uppercase + string.digits], 5)))
    # 舱单
    @property
    def get_bill(self):
        try:
            return time.strftime('%Y%m%d', time.localtime(time.time())) + "LJ" + str(self.billno).zfill(2)
        finally:
            self.billno = self.billno + 1


if __name__ == '__main__':
    c = BTOS_CustomData()
    t = BTOS_TempData()
