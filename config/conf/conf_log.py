# -*- coding: utf-8 -*-
# ------------Oooo---
# -----------(----)---
# ------------)--/----
# ------------(_/-
# ----oooO----
# ----(---)----
# -----\--(--
# ------\_)-
# ----
#     author : Yprisoner
#     email : yyprisoner@gmail.com
#                            ------
#    「 涙の雨が頬をたたくたびに美しく 」
import os
import logging
import logging.handlers
import tornado.log
from datetime import datetime

"""
    参数：作用
    %(levelno)s         打印日志级别的数值
    %(levelname)s       打印日志级别的名称
    %(pathname)s        打印当前执行程序的路径，其实就是sys.argv[0]
    %(filename)s        打印当前执行程序名
    %(funcName)s        打印日志的当前函数
    %(lineno)d          打印日志的当前行号
    %(asctime)s         打印日志的时间
    %(thread)d          打印线程ID
    %(threadName)s      打印线程名称
    %(process)d         打印进程ID
    %(message)s         打印日志信息
"""

LOG_CONF = dict(
    log_path="runtime/logs",  # 保存位置
    when="D",  # 以什么单位分割文件
    interval=1,  # 以上面的时间单位，隔几个单位分割文件
    backupCount=30,  # 保留多少历史记录文件
    format="%(asctime)s - %(name)s - %(filename)s[line:%(lineno)d] - %(levelname)s - %(message)s",
)


# 初始化日志管理
def init_log(log_filename="api", port=None, console_handler=False, file_handler=True, log_path=LOG_CONF['log_path'], base_level="INFO"):
    logger = logging.getLogger()
    logger.setLevel(base_level)
    # 配置控制台输出
    if console_handler:
        channel_console = logging.StreamHandler()
        channel_console.setFormatter(tornado.log.LogFormatter())
        logger.addHandler(channel_console)
    # 日志文件输出
    if file_handler:
        if not log_path:
            log_path = LOG_CONF['log_path']

        ### 日志分割 (根据月分割)
        log_path = log_path + datetime.now().strftime("/%Y-%m")
        if not os.path.exists(log_path): os.makedirs(log_path, 0o755)

        if log_filename:
            log_path = log_path + '/' + str(log_filename) + '_'
        if port:
            log_path = log_path + '@' + str(port)
        log_path = log_path + '.log'
        formatter = logging.Formatter(LOG_CONF['format'])
        channel_file = logging.handlers.TimedRotatingFileHandler(
            filename=log_path,
            when=LOG_CONF['when'],
            interval=LOG_CONF['interval'],
            backupCount=LOG_CONF['backupCount']
        )
        channel_file.setFormatter(formatter)
        logger.addHandler(channel_file)
