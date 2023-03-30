# -*- coding:utf-8 -*-
import psycopg2
from psycopg2 import Error
from Base.basepage import BasePage
from psycopg2.extras import RealDictCursor
from selenium import webdriver

class GetPg(BasePage):
    def __init__(self, driver):
        super(GetPg, self).__init__(driver)
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
        except Error as e:
            self.logger.error("Sql error:", exc_info=True)
        else:
            res = self.cur.fetchall()
            return res

