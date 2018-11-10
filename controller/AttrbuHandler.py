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
from service.AttrbuService import TagService, CategoryService
from tornado import gen
from model.models import Attributes


class CategoryHandler(BaseHandler):

    @gen.coroutine
    def get(self, arg=None, **kwargs):
        """
        查询分类
        :param categoryId: 分类ID 为空则查询分类列表
        :param kwargs:
        :return:
        """
        if arg is None:
            pager = Pager(self)
            count = self.db.query(Attributes).filter(Attributes.type == 'category').count()
            cateList = yield self.async_do(CategoryService.category_list, self.db, pager, count)
            self.json_return({
                'code': 0,
                'data': cateList
            })
        else:
            result = yield self.async_do(CategoryService.category,self.db, arg)
            self.json_return({
                'code':0,
                'data':self.to_dict(result)
            })

    @auth_required
    @gen.coroutine
    def post(self, *args, **kwargs):
        """
        添加分类
        :param args:
        :param kwargs:
        :return:
        """
        data = self.get_all_argument()
        result = yield self.async_do(CategoryService.add_category, self.db, data)
        if result['state']:
            self.save_log('添加分类', '添加分类 【{0}】 成功!'.format(data['name']))
            self.json_return({
                'code': 0,
                'msg': '添加分类 【{0}】 成功!'.format(data['name'])
            })
        else:
            self.json_return({
                'code': 9905,
                'error': result['message']
            })


    @auth_required
    @gen.coroutine
    def put(self, id=None, **kwargs):
        """
        更新分类
        :param id: 分类ID
        :param kwargs:
        :return:
        """
        if id:
            data = self.get_all_argument()
            result = yield self.async_do(CategoryService.update, self.db,id, data)
            if result:
                self.save_log('更新分类', '更新分类 【{0}】 成功!'.format(id))
                self.json_return({
                    'code':0,
                    'msg': '更新分类成功'
                })
            else:
                self.json_return({
                    'code': 9901,
                    'error':'更新分类失败'
                })
        else:
            self.error_return(400)

    @auth_required
    @gen.coroutine
    def delete(self, id=None, **kwargs):
        if id:
            result = yield self.async_do(CategoryService.del_category, self.db, id)
            if result:
                self.save_log('删除分类', '删除分类 【{0}】 成功!'.format(id))
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

"""
    标签
"""
class TagsHandler(BaseHandler):

    @gen.coroutine
    def get(self, *args, **kwargs):
        """
        查询Tag
        :param args:
        :param kwargs:
        :return:
        """
        pager = Pager(self)
        count = self.db.query(Attributes).filter(Attributes.type == 'tag').count()
        tagList = yield self.async_do(TagService.tag_list, self.db, pager, count)
        self.json_return({
            'code':0,
            'data': tagList
        })


    @auth_required
    @gen.coroutine
    def post(self, *args, **kwargs):
        """
        添加标签
        :param args:
        :param kwargs:
        :return:
        """
        data = self.get_all_argument()
        tagName = data['tagName'] if 'tagName' in data.keys() else None
        if tagName:
            result = yield self.async_do(TagService.add_tag, self.db, tagName)
            if result['state']:
                self.save_log('添加标签', '添加标签 【{0}】 成功!'.format(tagName))
                self.json_return({
                    'code': 0
                })
            else:
                self.json_return({
                    'code': 9905,
                    'error': result['message']
                })
        else:
            self.error_return(400)


    @auth_required
    @gen.coroutine
    def delete(self, tagName = None, **kwargs):
        """
        删除标签
        :param tagName: 要删除的标签的名称  为空则全部删除
        :param kwargs:
        :return:
        """
        result = yield self.async_do(TagService.del_tag, self.db, tagName)
        if result:
            self.save_log('删除标签', '删除标签 【{0}】 成功!'.format(tagName))
            self.json_return({
                'code': 0
            })
        else:
            self.json_return({
                'code': 9999,
                'error': '删除标签失败'
            })


