# -*- coding:utf-8 -*-
import atexit
import random
import string
import time
from datetime import datetime, timedelta

import yaml


class BtosTempData(object):
    _instance = None

    def __new__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self, filename=None):
        atexit.register(self.record)
        self.filename = filename
        with open(self.filename, encoding='utf-8') as f:
            data = yaml.load(f.read(), Loader=yaml.FullLoader)
            if data is not None:
                self.__dict__.update(data)

    def __getattribute__(self, item):
        """
        获取属性
        :param item: 属性名称
        :return: 值
        """
        return object.__getattribute__(self, item)

    def __setattr__(self, item, value):
        """
        定义属性
        :param item: 名称
        :param value: 值
        :return:
        """
        object.__setattr__(self, item, value)

    def __delattr__(self, item):
        """
        删除属性
        :param item: 属性名称
        :return:
        """
        object.__delattr__(self, item)

    def record(self):
        """
        存储属性
        :return:
        """
        with open(self.filename, "w+", encoding='utf-8') as f:  # 写文件
            yaml.safe_dump(data=self.__dict__, stream=f, allow_unicode=True)

    @property
    def print_data(self):
        """
        打印变量
        :return:
        """
        print(vars(self))
        return 0


class BtosCustomData(object):
    _instance = None

    def __new__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self):
        self.pktype = self.dict_pktype
        self.no = random.randint(0, 1000)

    @property
    def dict_pktype(self):
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
        return time.strftime('%m%d%H%M', time.localtime(time.time())) + "I"

    @property
    def get_Evoyage(self):
        return time.strftime('%m%d%H%M', time.localtime(time.time())) + "E"

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
        return "CD" + time.strftime('%Y%m%d', time.localtime(time.time())) + "LJ" + str(self.no).zfill(3)

    @property
    def get_mark(self):
        return "MT" + time.strftime('%Y%m%d', time.localtime(time.time())) + "LJ" + str(self.no).zfill(3)

    @property
    def get_ht(self):
        return "HT" + time.strftime('%Y%m%d', time.localtime(time.time())) + "LJ" + str(self.no).zfill(3)

    @property
    def get_gtwg(self):
        return round(random.uniform(200, 8000), 3)

    @property
    def get_gtpks(self):
        return random.randint(10, 3000)

    @property
    def get_gtvol(self):
        return random.randint(0, 3000)

    @property
    def get_datetime_now(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def get_datetime_add(t, day=0, hour=0, minute=0):
        return (datetime.strptime(t, "%Y-%m-%d %H:%M:%S") + timedelta(days=day, hours=hour, minutes=minute)) \
            .strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def to_date(t):
        return (datetime.strptime(t, "%Y-%m-%d %H:%M:%S")).strftime("%Y-%m-%d 00:00:00")

    @property
    def get_phone(self):
        second = [3, 4, 5, 7, 8][random.randint(0, 4)]
        third = {
            3: random.randint(0, 9),
            4: [5, 7, 9][random.randint(0, 2)],
            5: [i for i in range(10) if i != 4][random.randint(0, 8)],
            7: [i for i in range(10) if i not in [4, 9]][random.randint(0, 7)],
            8: random.randint(0, 9)
        }[second]
        suffix = ''
        for x in range(8):
            suffix = suffix + str(random.randint(0, 9))
        return "1{}{}{}".format(second, third, suffix)
