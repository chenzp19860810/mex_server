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
import redis
import tornado.gen

class SessionManger:

    def __init__(self, options):
        self.connection_pool = None
        self.options = options
        self.session_key_name = options['session_key_name']
        self.session_expires_days = options['session_expires_days']

    # redis连接池
    def get_connection_pool(self):
        if not self.connection_pool:
            self.connection_pool = redis.ConnectionPool(host=self.options['host'],port=self.options['port'],password=self.options['password'],max_connections=self.options['max_connections'])
        return self.connection_pool

    # 连接对象
    @tornado.gen.coroutine
    def get_redis_client(self):
        connection_pool = self.get_connection_pool()
        client = redis.StrictRedis(connection_pool=connection_pool)
        raise tornado.gen.Return(client)
