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
import logging
from config.config import MOBPUSH
from extends.mobpush.push import push as Push, tools

logger = logging.getLogger(__name__)

"""
    推送消息到站长移动端APP
"""


class MessageManager:
    mobpush = None

    def __init__(self):
        self.mobpush = Push()

    def push(self, content):
        # 初始化推送
        panel = self.mobpush.initPush(appkey=MOBPUSH['AppKey'], content=content, plats=[1])
        # 设置推送范围
        target = self.mobpush.buildTarget(target=1, tags=None, alias=None, registrationIds=None, city=None, block=None)
        # 设置Android定制信息
        android = self.mobpush.buildAndroid(androidTitle='SS来消息了')
        # 设置推送扩展信息
        extra = self.mobpush.buildExtra(unlineTime=1)
        js = tools().json_join(panel, target)
        js = tools().json_join(js, android)
        js = tools().json_join(js, extra)
        try:
            result = self.mobpush.sendPush(js)
            print("================MobPush Start===================")
            print(result)
            print("================MobPush End===================")
        except Exception as e:
            logger.error(e)