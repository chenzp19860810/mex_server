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
from model.models import to_dict

"""
    公共分页类
    page        当前页面
    pageSize    页面显示数量
    totalPage   总页数
    totalCount    总分页数
    offset      查询偏移量

    使用
    查询的时候先赋值总数量
"""


class Pager:
    ### 默认分页数据数量
    default_pageSize = 10
    ### 默认的总页数
    totalPage = 1
    ### 默认数据的数量
    totalCount = 0

    # 初始化
    def __init__(self, request):
        ### 获取当前page页面
        self.page = int(request.get_argument("page", 1))
        ### 获取每页查询的数量
        self.pageSize = int(request.get_argument("pageSize", self.default_pageSize))

    # 是否存在上一页
    def has_prev(self):
        return self.page > 1

    # 是否存在下一页
    def has_next(self):
        return self.page < self.totalPage

    def set_total_count(self, count):
        ### 设置数据总数
        self.totalCount = count
        ### 设置有多少页
        if self.totalCount > 0 and self.pageSize != 0:
            self.totalPage = int(self.totalCount / self.pageSize) if self.totalCount % self.pageSize == 0 else int(self.totalCount / self.pageSize) + 1

    # 查询数据
    def build_query(self, query):
        if self.pageSize != 0:
            ### 获取查询偏移量
            offset = (self.page - 1) * self.pageSize if self.page > 0 else 0
            ### 返回query对象
            queryData = query.limit(self.pageSize).offset(offset).all()
        else:
            queryData = query.all()

        result = {
            'list': to_dict(queryData),
            'nextStart': self.page + 1 if self.has_next() else 0,
            'pageSize': self.pageSize,
            'totalNum': self.totalCount,
            'hasMore': self.has_next()
        }

        return result
