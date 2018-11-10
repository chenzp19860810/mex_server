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
import logging
from config.conf.conf_db import redis_config

logger = logging.getLogger(__name__)

def clear_cache():
    cache = redis.Redis(host=redis_config['host'], port=redis_config['port'])
    for key in cache.keys():
        keystr = str(key, encoding='UTF-8')
        if 'mex_article' in keystr:
            cache.delete(keystr)
    logger.info(" === 清除缓存成功 === ")

if __name__ == '__main__':
    clear_cache()