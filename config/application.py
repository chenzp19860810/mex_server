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
import tornado.web
import concurrent.futures
from .config import DEBUG
from service.Cache import CacheManger
from service.Session import SessionManger
from service.Message import MessageManager
from config.conf.conf_db import redis_config, init_db_pool
from config.conf.conf_folder import init_folder

"""
    这里开始使用的是传统的方法返回application的
    不过后来看了别人写的代码就回来重构了
    继承会把父类的公开属性方法保留下来
    可以在这里进行全局的配置 后续开发会方便很多
    
    这里增加了一个 kwargs 参数，可以自定义传入配置
"""

# App配置
settings = dict(
    debug=DEBUG,
    serve_traceback=DEBUG,  # 错误跟踪
    xsrf_cookies=True,  # 开启 xsrf Token
    cookie_secret="YzY1MzFlZDJkZGNkMDg0YTY0ZjU1YTdmMzRiOWY2MGU="
)


class Application(tornado.web.Application):
    def __init__(self, url_handler, **kwargs):
        args = dict(settings, **kwargs)
        super(Application, self).__init__(handlers=url_handler, **args)
        init_folder()
        ### 异步线程池
        self.thread_executor = concurrent.futures.ThreadPoolExecutor(1024)
        ### 数据库连接池
        self.db_pool = init_db_pool()
        ### 缓存控制
        self.cache_manager = CacheManger(redis_config)
        ### Session控制
        self.session_manager = SessionManger(redis_config)
        ### 消息推送
        self.message_manager = MessageManager()