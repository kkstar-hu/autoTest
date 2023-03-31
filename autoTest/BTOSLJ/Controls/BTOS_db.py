# -*- coding:utf-8 -*-
import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2 import Error
from Commons.log import getlogger
import pandas as pd
from prettytable import from_db_cursor

class GetPg():
    def __init__(self):
        self.logger = getlogger()
        try:
            self.conn = psycopg2.connect(database="btopsdb", user="btops",password="tCXd#0DWK-brIk", host="10.166.0.137", port="6432")
        except Error as e:
            self.logger.error("Error while connecting PostgreSQL:", exc_info=True, stack_info=False)
        else:
            self.cur = self.conn.cursor(cursor_factory = RealDictCursor)

    def __del__(self):
        self.cur.close()
        self.conn.close()

    def execute_sql(self, sql : str):
        try:
            self.cur.execute(sql)
            self.conn.commit()
        except Error:
            self.conn.rollback()
            self.logger.error("Sql error:", exc_info=True)


