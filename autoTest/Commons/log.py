import logging
import os
from Commons.DateTime import DataTime

def getlogger():
    #创建日志器
    logger=logging.getLogger('MYLOG')
    logger.setLevel('INFO')
    if not logger.handlers:
        log_name = log_file()
        file_handler = logging.FileHandler(log_name, encoding="utf-8")  #定义处理器。控制台和文本输出两种方式
        console_handler=logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s %(filename)s [line:%(lineno)d]: %(message)s')  #设置不同的输出方式
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)    #日志器添加处理器
        logger.addHandler(console_handler)
    return logger

def log_file():
    """日志目录"""
    log_dir = os.path.join(os.path.join(os.getcwd()), 'logs')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    now_date = DataTime.Get_Current_Date()
    now_log_path = os.path.join(log_dir, f'{now_date}')
    if not os.path.exists(now_log_path):
        os.makedirs(now_log_path)
    now_time = DataTime.Get_Current_Time_Format('%Y%m%d-%H%M%S')
    log_name = os.path.join(now_log_path, f'{now_time}.log')
    return log_name

