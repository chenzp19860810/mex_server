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
from tornado import gen

class CacheManger:

    """
        缓存控制
    """

    def __init__(self, options):
        self.connection_pool = None
        self.options = options
        self.client = None

    def get_connection_pool(self):
        """
        获取redis连接
        :return:
        """
        if not self.connection_pool:
            self.connection_pool = redis.ConnectionPool(host=self.options['host'],port=self.options['port'],password=self.options['password'],max_connections=self.options['max_connections'])
        return self.connection_pool


    @gen.coroutine
    def get_redis_client(self):
        connection_pool = self.get_connection_pool()
        client = redis.StrictRedis(connection_pool=connection_pool)
        raise gen.Return(client)

    @gen.coroutine
    def fetch_client(self):
        self.client = yield self.get_redis_client()


    def update_expire_time(self):
        pass

    @gen.coroutine
    def set(self, name=None, key=None,value=None, expire_time=None):
        yield self.fetch_client()
        if self.client:
            if name is None:
                self.client.set(key, value)
            else:
                self.client.hset(name,key,value)
            if expire_time is not None:
                self.client.expire(key, expire_time)

    @gen.coroutine
    def get(self, name=None, key=None):
        yield self.fetch_client()
        if self.client:
            if name is None:
                return self.client.get(key)
            else:
                return self.client.hget(name, key)

    @gen.coroutine
    def remove(self, key):
        yield self.fetch_client()
        if self.client:
            self.client.delete(key)