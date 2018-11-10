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


class BaseService:

    @staticmethod
    def query_pager(query, pager, count=None):
        if count:
            ### 传入总数
            pager.set_total_count(count)
        else:
            ### 默认查询
            pager.set_total_count(query.count())
        result = pager.build_query(query)
        return result
