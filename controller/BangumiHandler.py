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
from controller import BaseHandler, auth_required
from model.pager import Pager
from tornado import gen
from service.BnagumiService import BangumiService


class BangumiHandler(BaseHandler):

    @gen.coroutine
    def get(self, *args, **kwargs):
        """
        查询列表
        :param args:
        :param kwargs:
        :return:
        """
        pager = Pager(self)
        result = yield self.async_do(BangumiService.bangumi_list, self.db, pager)
        self.json_return({
            'code': 0,
            'data': self.to_dict(result)
        })


    @auth_required
    @gen.coroutine
    def post(self, *args, **kwargs):
        """
        添加番剧
        :param args:
        :param kwargs:
        :return:
        """
        data = self.get_all_argument()
        result = yield self.async_do(BangumiService.add_bangumi, self.db, data)
        if result:
            self.json_return({
                'code': 0,
                'msg': '添加成功'
            })
        else:
            self.json_return({
                'code': 9901,
                'error': '添加失败'
            })


    @auth_required
    @gen.coroutine
    def put(self, bgmId=None, **kwargs):
        """
        更新番剧
        :param bgmId:
        :param kwargs:
        :return:
        """
        if bgmId is None:
            self.error_return(400)
        else:
            data = self.get_all_argument()
            progress = int(data['progress'])
            result = yield self.async_do(BangumiService.update_bangumi, self.db, bgmId, progress)
            if result:
                self.json_return({
                    'code': 0,
                    'msg': '更新进度成功'
                })
            else:
                self.json_return({
                    'code': 9901,
                    'error': '更新进度失败'
                })


    @auth_required
    @gen.coroutine
    def delete(self, bgmId=None, **kwargs):
        if bgmId is None:
            self.error_return(400)
        else:
            result = yield self.async_do(BangumiService.del_bangumi, self.db, bgmId)
            if result:
                self.json_return({
                    'code':0,
                    'msg':'删除成功'
                })
            else:
                self.json_return({
                    'code': 9901,
                    'error': '删除失败'
                })