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
import json
import logging
from tornado import gen
from model.models import to_dict
from service.ArticleService import ArticleService
from config.conf.conf_db import redis_cache_keys

logger = logging.getLogger(__name__)

'''
    全站数据缓存
    CacheService 缓存策略
        站点缓存，加快访问速度
        查询策略:先查询redis缓存，未命中查询数据库
        更新策略:数据写入数据库后，更新redis缓存
'''

class CacheService:


    @staticmethod
    @gen.coroutine
    def query_article_cache(db_session,  cache_manager, async_do, id):
        """
        查询缓存
        :param db_session:
        :param cache_manager:
        :param async_do:
        :param id:
        :return:
        """
        cache = yield cache_manager.get(redis_cache_keys['cache_article_key'].format(id))
        if cache is not None:
            gen.Return(json.loads(cache))
        else:
            result = yield async_do(ArticleService.query_article, db_session, id)
            if result is not None:
                yield async_do(CacheService.update_article_cache, db_session, cache_manager, async_do, id)
                gen.Return(result)
            else:
                gen.Return(None)


    @staticmethod
    @gen.coroutine
    def update_article_cache(db_session, cache_manager, async_do , id):
        """
        更新 或者 添加文章缓存
        :param cache_manager: 缓存控制
        :param async_do: 异步
        :param db_session: 数据库连接
        :param id: 文章查询标识id
        :return:
        """
        result = yield async_do(ArticleService.query_article, db_session, id)
        if not result is None:
            if isinstance(result, dict):
                yield async_do(cache_manager.set, redis_cache_keys['cache_article_key'].format(id), json.dumps(result))
                # cache_manager.set(redis_cache_keys['cache_article_key'].format(id), json.dumps(result))
            else:
                try:
                    yield async_do(cache_manager.set, redis_cache_keys['cache_article_key'].format(id), json.dumps(to_dict(result)))
                    # cache_manager.set(redis_cache_keys['cache_article_key'].format(id), json.dumps(to_dict(result)))
                except Exception as e:
                    logger.error('添加文章缓存失败  {0}'.format(e))
