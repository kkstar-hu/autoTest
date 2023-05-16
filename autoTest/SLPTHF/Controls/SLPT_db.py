import cx_Oracle as oracle
from cx_Oracle import Error as e1
from Commons.log import getlogger

class ConnectDb():
    def __init__(self, host):
        self.logger = getlogger()
        try:
            if host=='10.166.0.156':
                # 如果这一步报错就去oracle官网下载21版本的client，并将解压文件中所有后缀为dll的文件复制到本地python安装目录下
                self.conn=oracle.connect('YLPTTEST/asuDf#aTESZ7@10.166.0.156:1521/ylpttest')#TODO
                print(self.conn)
                self.cursor=self.conn.cursor()
        except e1:
            self.logger.error("Error while connecting PostgreSQL:", exc_info=True, stack_info=False)

    def __del__(self):
        self.cursor.close()
        self.conn.close()

    def execute_sql(self, sql: str):
        try:
            self.conn.execute(sql)
            self.conn.commit()
        except e1:
            self.conn.rollback()
            self.logger.error("Sql error:", exc_info=True)

    def select_sql(self, sql: str):
        try:
            all=self.cursor.execute(sql)
            return all
        except e1:
            self.logger.error("Sql error:", exc_info=True)


if __name__ == '__main__':
    db=ConnectDb('10.166.0.156')
