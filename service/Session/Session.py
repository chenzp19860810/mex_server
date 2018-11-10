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
import hashlib
import json
import time
from tornado import gen
from extends.utils import get_random_str


# 封装Session

class Session(dict):
    def __init__(self, request_handler):
        super(Session, self).__init__()
        self.session_id = None
        self.session_manager = request_handler.application.session_manager
        self.request_handler = request_handler
        self.client = None

    @gen.coroutine
    def init_fetch(self):
        """
        初始化连接
        :return:
        """
        self.client = yield self.session_manager.get_redis_client()
        yield self.fetch_client()

    def get_session_id(self):
        """
        :return:
        """
        if not self.session_id:
            self.session_id = self.request_handler.get_secure_cookie(self.session_manager.session_key_name)
        return self.session_id

    def generate_session_id(self):
        """
        用户访问的唯一ID
        如果第一次访问网站
        设置cookies
        :return:
        """
        if not self.get_session_id():
            self.session_id = str(get_random_str())
            self.request_handler.set_secure_cookie(self.session_manager.session_key_name, self.session_id,
                                                   expires_days=self.session_manager.session_expires_days)
        return self.session_id

    @gen.coroutine
    def fetch_client(self):
        if self.get_session_id():
            data = self.client.get(self.session_id)
            if data:
                self.update(json.loads(data))

    @gen.coroutine
    def save(self, expire_time=None):
        """
        保存 session 到 redis
        :param expire_time:
        :return:
        """
        session_id = self.generate_session_id()
        data_json = json.dumps(self)
        self.client.set(session_id, data_json)
        if expire_time:
            self.client.expire(session_id, expire_time)