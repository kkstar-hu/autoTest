import cx_Oracle
from Commons.log import getlogger

class ConnectDb():
    def __init__(self, host):
        self.logger = getlogger()
        if host=='10.166.0.156':

            self.conn=cx_Oracle.connect('YLPTTEST','asuDf#aTESZ7','10.166.0.156:1521/ylpttest')
            self.cursor=self.conn.cursor()
            #TODO
    # def __del__(self):
    #     self.conn.close()

if __name__ == '__main__':
    db=ConnectDb('10.166.0.156')
