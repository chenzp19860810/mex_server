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
import socket
import tornado.ioloop
import tornado.httpserver
from urls import url_api
from config.application import Application
from config.config import DEBUG
from config.conf.conf_log import init_log
from service.TimeTask import init_task
from tornado.options import define, options, parse_command_line

"""
    命令行执行  python server.py --port=9900
"""
define("port", default=9900, help="服务运行端口 ", type=int)


# 启动API服务
def run_server():
    # 加载命令行
    parse_command_line()
    # 加载日志配置
    init_log(port=options.port, console_handler=DEBUG)
    # 启动服务
    app = Application(url_handler=url_api)
    tornado.httpserver.HTTPServer(app, xheaders=True).listen(options.port)
    loop = tornado.ioloop.IOLoop.instance()
    # 加载定时任务
    init_task()
    if DEBUG:
        ip = socket.gethostbyname(socket.gethostname())
        print('server is running at http://%s:%s' % (ip, options.port))
    loop.start()


if __name__ == '__main__':
    run_server()