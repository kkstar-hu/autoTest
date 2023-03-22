import logging
import os
import time


def getlogger():
#创建日志器
    logger=logging.getLogger('MYLOG')

    logger.setLevel('INFO')

    if not logger.handlers:
    #定义处理器。控制台和文本输出两种方式
        console_handler=logging.StreamHandler()
        file_handler = logging.FileHandler(os.path.join(os.getcwd(),'Log.txt'), mode='a', encoding="utf-8")
        #设置不同的输出方式
        console_fmt = "%(asctime)s--->%(levelname)s--->%(message)s"
        file_fmt = "%(asctime)s--->%(levelname)s--->%(message)s"

        #格式
        fmt1=logging.Formatter(fmt=console_fmt)
        fmt2=logging.Formatter(fmt=file_fmt)

        console_handler.setFormatter(fmt1)
        file_handler.setFormatter(fmt2)


            #日志器添加处理器
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)


    return logger


class Log:
    def __init__(self,logger=None):
        self.logger = logging.getLogger(logger)
        self.logger.setLevel(logging.INFO)
        # 创建一个handler，用于写入日志文件
        log_name = self.log_file()
        fh = logging.FileHandler(log_name)
        fh.setLevel(logging.INFO)
        # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        # 定义handler的输出格式
        formatter = logging.Formatter('%(asctime)s - %(levelname)s %(filename)s [line:%(lineno)d]: %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        # 给logger添加handler
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)


    def log_file(self):
        """日志目录"""
        log_dir = os.path.join(os.path.join(os.getcwd()), 'logs')
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        now_date = self.now_date()
        now_log_path = os.path.join(log_dir, f'{now_date}')
        if not os.path.exists(now_log_path):
            os.makedirs(now_log_path)
        now_time = self.now_time()
        log_name = os.path.join(now_log_path, f'{now_time}.log')
        return log_name

    def now_date(self):
        return time.strftime('%Y-%m-%d', time.localtime(time.time()))

    def now_time(self):
        return time.strftime('%Y%m%d-%H%M%S', time.localtime(time.time()))


logger = Log().logger