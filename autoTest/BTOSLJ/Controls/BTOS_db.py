# -*- coding:utf-8 -*-
import json
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy import create_engine, text
import pymysql
from pymysql import Error as e2
from psycopg2 import Error as e1
from Commons.log import getlogger
import pandas as pd
import urllib.parse


class GetPg():
    def __init__(self, host):
        self.logger = getlogger()
        self.engine = None
        try:
            if (host == "10.166.0.137"):
                self.engine = create_engine('postgresql://%s:%s@%s:%s/%s'
                                            % ("btops", "tCXd#0DWK-brIk", "10.166.0.137", "6432", "btopsdb"))
            elif (host == "10.116.8.20"):
                self.engine = create_engine('mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8'
                                            % ("root", urllib.parse.quote_plus("nezha@2023"), "10.116.8.20", "9030",
                                               "ODS"))
        except e1:
            self.logger.error("Error while connecting PostgreSQL:", exc_info=True, stack_info=False)
        except e2:
            self.logger.error("Error while connecting MySQL:", exc_info=True, stack_info=False)
        else:
            self.conn = self.engine.connect()

    def __del__(self):
        self.conn.close()

    def execute_sql(self, sql: str):
        try:
            self.conn.execute(sql)
            self.conn.commit()
        except (e1, e2):
            self.conn.rollback()
            self.logger.error("Sql error:", exc_info=True)

    # 仅用于select
    def read_from_table(self, filename: str):
        pd.set_option('display.max_columns', 20)
        pd.set_option('display.max_rows', 20)
        sql = text(self.load_sql(filename))
        data = pd.read_sql(sql, self.conn)
        return data

    # 仅用于select
    def select_from_table(self, sql: str):
        sql = text(sql)
        res = pd.read_sql(sql, self.conn)
        return res

    def load_sql(self, filename: str):
        try:
            with open(filename, encoding='utf-8', mode='r') as f:
                return f.read()
        except Exception:
            self.logger.error("读取文件失败:{}".format(filename), exc_info=True)

    def to_json(self, res):
        res = res.to_json(orient='records', force_ascii=False)
        if (type(res) != type(dict())):
            res = json.loads(res)
        return json.dumps(res, indent=4, ensure_ascii=False)

    def to_json_dict(self, res):
        res = res.to_json(orient='records', force_ascii=False)
        if (type(res) != type(dict())):
            res = json.loads(res)
        return res





