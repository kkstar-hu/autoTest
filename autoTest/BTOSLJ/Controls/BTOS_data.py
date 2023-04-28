# -*- coding:utf-8 -*-
import random
import string
import time
from datetime import datetime, timedelta
from decimal import Decimal


class BTOS_TempData(object):
    _instance = None

    # 单例模式
    def __new__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self, filename=None):
        self.filename = filename
        self.file_obj = open(self.filename, mode='r', encoding='utf-8')
        data = self.file_obj.read().splitlines()
        self.file_obj.close()
        d = dict()
        for line in data:
            key, value = line.split('=')
            d[key] = value
        self.__dict__.update(d)
        self.file_w = open(self.filename, mode='w', encoding='utf-8')

    # 获取属性
    def __getattribute__(self, item):
        return object.__getattribute__(self, item)

    # 定义属性
    def __setattr__(self, item, value):
        object.__setattr__(self, item, value)

    # 删除属性
    def __delattr__(self, item):
        object.__delattr__(self, item)

    # 存储变量
    def __del__(self):
        for (key, value) in self.__dict__.items():
            if key != 'filename' and key != 'file_obj' and key != 'file_w':
                self.file_w.write(str(key)+'='+str(value)+'\n')
        self.file_w.close()

    # 打印变量
    @property
    def print_data(self):
        print(vars(self))


class BTOS_CustomData(object):
    _instance = None
        # 单例模式
    def __new__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self):
        self.pktype = self.dict_pktype()
        self.billno = 1
        self.markno = 1

    @staticmethod
    def dict_pktype():
        d = dict()
        d["041303"] = "11"
        d["124"] = "14"
        d["0417"] = "1"
        d["049002"] = "9"
        d["041108"] = "9"
        d["1511"] = "16"
        d["041501"] = "9"
        d["04121"] = "1"
        d["041102"] = "2"
        d["011"] = "11"
        d["C01"] = "14"
        return d

    # 根据货名获取包装
    @property
    def get_pktype(self):
        gtypecd = random.choice(list(self.pktype.keys()))
        return gtypecd, self.pktype.get(gtypecd)

    # 航次
    @property
    def get_Ivoyage(self):
        return "B" + time.strftime('%m%d', time.localtime(time.time())) + "I"

    def get_Evoyage(self):
        return "B" + time.strftime('%m%d', time.localtime(time.time())) + "E"

    # 车牌号
    @property
    def get_license_plate(self):
        q1 = "鲁京津沪浙苏冀豫辽吉黑渝蒙桂宁藏新港澳赣皖闵粤贵云鄂湘川琼晋陕甘青台"
        return '{}{}'.format(random.choice(q1) + random.choice(string.ascii_uppercase),
                             "".join(
                                 random.sample([x for x in string.digits + string.ascii_uppercase + string.digits], 5)))

    # 舱单
    @property
    def get_bill(self):
        try:
            return "CD" + time.strftime('%Y%m%d', time.localtime(time.time())) + "LJ" + str(self.billno).zfill(2)
        finally:
            self.billno = self.billno + 1

    @property
    def get_mark(self):
        try:
            return "MT" + time.strftime('%Y%m%d', time.localtime(time.time())) + "LJ" + str(self.markno).zfill(2)
        finally:
            self.markno = self.markno + 1

    @property
    def get_gtwg(self):
        return random.randint(200, 8000)

    @property
    def get_gtpks(self):
        return random.randint(100, 3000)

    @property
    def get_gtvol(self):
        return random.randint(0, 3000)

    @property
    def get_datetime_now(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


    def get_datetime_add(self, time, day=0, hour=0, minute=0):
        return (datetime.strptime(time, "%Y-%m-%d %H:%M:%S") + timedelta(days=day, hours=hour, minutes=minute))\
            .strftime("%Y-%m-%d %H:%M:%S")

    def to_date(self, time):
        return (datetime.strptime(time, "%Y-%m-%d %H:%M:%S")).strftime("%Y-%m-%d 00:00:00")


if __name__ == '__main__':
    c = BTOS_CustomData()
    t = BTOS_TempData()
