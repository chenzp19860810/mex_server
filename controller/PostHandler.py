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
from config.config import DEBUG
from controller import BaseHandler, auth_required
from tornado import gen
from model.pager import Pager
from service.ArticleService import ArticleService
from config.conf.conf_db import redis_cache_keys

logger = logging.getLogger(__name__)

"""
    主要的文章控制
"""


class ArticleHandler(BaseHandler):

    @gen.coroutine
    def get(self, action=None, **kwargs):
        """
        GET 查询
        :param articleId: article ID 为空则查询分页列表
        :param kwargs:
        :return:
        """
        if action is None:
            ### 后台查询
            yield self.admin_select_articleList()
        elif action == 'list':
            yield self.home_select_articleList()
        elif action == 'category':
            yield self.home_select_articleListByCategory()
        else:
            if action.isdigit():
                yield self.select_article(action)
            else:
                self.error_return(400)



    @gen.coroutine
    def home_select_articleList(self):
        """
        前台文章列表查询
        不需要权限
        :return:
        """
        page = self.get_argument("page", 1)
        pageSize = self.get_argument("pageSize", 6)
        if pageSize.isdigit() and int(pageSize) == 6:
            cache_article_list = yield self.cache_manager.get(key=redis_cache_keys['cache_article_pages_key'].format(int(page)))
            if DEBUG:
                print("============分页缓存结果=============")
                print(cache_article_list)
                print("============分页缓存结果 END=============")
            if cache_article_list is None:
                pager = Pager(self)
                articleList = yield self.async_do(ArticleService.home_article_list, self.db, pager)
                if DEBUG:
                    print("============分页查询结果=============")
                    print(articleList)
                    print("============分页查询结果 END=============")
                if articleList['list'] is not None: ### 缓存 3 天
                    yield self.cache_manager.set(key=redis_cache_keys['cache_article_pages_key'].format(int(page)),
                                           value=json.dumps(self.to_dict(articleList)), expire_time=3600*24*3)
            else:
                articleList = json.loads(cache_article_list)

            if articleList['list'] is not None:
                for item in articleList['list']:
                    item['post_markdown'] = item['post_markdown'][0:270] + '......'
            self.json_return({
                'code': 0,
                'data': self.to_dict(articleList)
            })
        else:
            pager = Pager(self)
            articleList = yield self.async_do(ArticleService.home_article_list, self.db, pager)
            if DEBUG:
                print("============分页查询结果【pageSize ！= 6】=============")
                print(articleList)
                print("============分页查询结果【pageSize ！= 6】 END=============")
            if articleList['list'] is not None:
                for item in articleList['list']:
                    item['post_markdown'] = item['post_markdown'][0:270] + '......'
            self.json_return({
                'code': 0,
                'data': self.to_dict(articleList)
            })


    @gen.coroutine
    def home_select_articleListByCategory(self):
        """
        根据分类查询文章列表
        :return:
        """
        pager = Pager(self)
        where = self.get_argument('category', None)
        articleList = yield self.async_do(ArticleService.home_article_list, self.db, pager, where)
        if articleList['list'] is not None:
            for item in articleList['list']:
                item['post_markdown'] = item['post_markdown'][0:270] + '......'
        self.json_return({
            'code': 0,
            'data': self.to_dict(articleList)
        })

    @gen.coroutine
    def select_article(self, action):
        """
        查询单篇文章内容
        缓存 Redis
        :return:
        """
        cache_article = yield self.cache_manager.get(key=redis_cache_keys['cache_article_key'].format(int(action)))
        # cache_article = str(cache_article, encoding='UTF-8')
        if DEBUG:
            print("============缓存结果=============")
            print(cache_article)
            print("============缓存结果 END=============")
        if cache_article is None or cache_article == 'null':
            result = yield self.async_do(ArticleService.query_article, self.db, action)
            if DEBUG:
                print("============查询结果=============")
                print(result)
                print("============查询结果 END=============")
            if result is not None:
                yield self.cache_manager.set(key=redis_cache_keys['cache_article_key'].format(int(action)),
                                       value=json.dumps(self.to_dict(result)), expire_time=self.session_expire_time)
        else:
            result = json.loads(cache_article)
        self.json_return({
            'code': 0,
            'data': self.to_dict(result)
        })

    @auth_required
    @gen.coroutine
    def admin_select_articleList(self):
        """
        后台文章列表查询
        加权限
        :return:
        """
        pager = Pager(self)
        articleList = yield self.async_do(ArticleService.article_list, self.db, pager, None,
                                          self.get_argument('post_status', 'publish'))
        self.json_return({
            'code': 0,
            'data': self.to_dict(articleList)
        })


    @gen.coroutine
    def post(self, arg=None, **kwargs):
        """
        添加文章
        :param args:
        :param kwargs:
        :return:
        """
        if arg is None:
            yield self.admin_add_article()
        else:
            if arg =='v':
                yield self.update_article_views()
            else:
                self.error_return(400)


    @gen.coroutine
    def update_article_views(self):
        """
        更新文章浏览数 前台 不需要权限
        :return:
        """
        try:
            data = self.get_all_argument()
            article_id = data['id']
            if article_id is not None and article_id.isdigit():
                result = yield self.async_do(ArticleService.update_article_views, self.db, int(article_id))
                if result:
                    self.json_return({
                        'code': 0,
                        'msg': 'success'
                    })
                else:
                    self.json_return({
                        'code': 1,
                        'error': 'error'
                    })
            else:
                self.error_return(400)
        except Exception as e:
            self.error_return(405)

    @auth_required
    @gen.coroutine
    def admin_add_article(self):
        """
        添加文章 后台 需要权限
        :return:
        """
        data = self.get_all_argument()
        try:
            result = yield self.async_do(ArticleService.add_article, self.db, data)
            if result is not False:
                yield self.cache_manager.set(key=redis_cache_keys['cache_article_key'].format(int(result)),
                                             value=json.dumps(self.to_dict(result)),
                                             expire_time=self.session_expire_time)
                self.save_log('添加文章', '添加文章 【{}】 成功!'.format(data['post_title']))
                self.json_return({
                    'code': 0,
                    'msg': '添加文章 【{}】 成功!'.format(data['post_title'])
                })
            else:
                self.json_return({
                    'code': 9901,
                    'error': '添加文章 【{}】 失败!'.format(data['post_title'])
                })
        except Exception as e:
            logger.error('添加文章失败! {}'.format(e))
            self.error_return(400)


    @auth_required
    @gen.coroutine
    def put(self, method=None, **kwargs):
        """
        更新文章
        :param articleId:
        :param kwargs:
        :return:
        """
        if method == 'reduction':
            ### 回收站还原
            data = self.get_all_argument()
            id = data['id']
            result = yield self.async_do(ArticleService.update_article, self.db, id)
            if result:
                self.json_return({
                    'code': 0,
                    'msg': '还原成功'
                })
            else:
                self.json_return({
                    'code': 9901,
                    'error': '还原失败'
                })
        elif method == 'remove':
            ### 添加到回收站
            data = self.get_all_argument()
            id = data['id']
            result = yield self.async_do(ArticleService.remove_article, self.db, id)
            if result:
                self.json_return({
                    'code': 0,
                    'msg': '移动到回收站成功'
                })
            else:
                self.json_return({
                    'code': 9901,
                    'error': '移动到回收站失败'
                })
        else:
            ### 更新内容
            if method.isdigit():
                result = yield self.async_do(ArticleService.update_article, self.db, method, self.get_all_argument())
                if result:
                    yield self.cache_manager.remove(key=redis_cache_keys['cache_article_key'].format(int(method)))
                    self.json_return({
                        'code': 0,
                        'msg': '更新成功'
                    })
                else:
                    self.json_return({
                        'code': 9901,
                        'error': '更新失败'
                    })
            else:
                self.error_return(400)

    @auth_required
    @gen.coroutine
    def delete(self, articleId=None, **kwargs):
        """
        删除
        :param articleId: 要删除的文章ID
        :param kwargs:
        :return:
        """
        if articleId:
            result = yield self.async_do(ArticleService.del_article, self.db, articleId)
            if result:
                yield self.cache_manager.remove(key=redis_cache_keys['cache_article_key'].format(int(articleId)))
                self.json_return({
                    'code': 0,
                    'msg': '删除成功'
                })
            else:
                self.json_return({
                    'code': 9901,
                    'error': '删除失败'
                })
        else:
            self.error_return(400)