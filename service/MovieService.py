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
from . import BaseService
from model.models import Movies

logger = logging.getLogger(__name__)


class MovieService:


    @staticmethod
    def movie_list(db_session, pager, count=None):
        """
        movie list
        :param db_session:
        :param pager:
        :param count:
        :return:
        """
        query = db_session.query(Movies)
        return BaseService.query_pager(query, pager, count)
