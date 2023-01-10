import logging
import os


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