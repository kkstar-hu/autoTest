import logging
import os
import time


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
        phone_log_path = os.path.join(log_dir, f'{now_date}')
        if not os.path.exists(phone_log_path):
            os.makedirs(phone_log_path)
        now_time = self.now_time()
        log_name = os.path.join(phone_log_path, f'{now_time}.log')
        return log_name

    def now_date(self):
        return time.strftime('%Y-%m-%d', time.localtime(time.time()))

    def now_time(self):
        return time.strftime('%Y%m%d-%H%M%S', time.localtime(time.time()))

