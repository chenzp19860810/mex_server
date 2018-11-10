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
from model.models import Bangumis

logger = logging.getLogger(__name__)

class BangumiService:


    @staticmethod
    def bangumi_list(db_session, pager, count=None):
        """
        List
        :param db_session:
        :param pager:
        :param count:
        :return:
        """
        query = db_session.query(Bangumis)
        return BaseService.query_pager(query, pager, count)


    @staticmethod
    def add_bangumi(db_session, data):
        """
        Add
        :param db_session:
        :param data:
        :return:
        """
        bgm = Bangumis(
            title=data['title'].strip(),
            description=data['description'].strip(),
            cover=data['cover'],
            total=data['total'],
            progress=data['progress'],
            share_url=data['share_url']
        )
        try:
            db_session.add(bgm)
            db_session.commit()
            logger.info('添加番剧 【{}】 成功!'.format(bgm.title))
            return True
        except Exception as e:
            db_session.rollback()
            logger.error('添加番剧 【{}】 失败! {}'.format(bgm.title, e))
            return False


    @staticmethod
    def update_bangumi(db_session, id, progress):
        """
        update
        :param db_session:
        :param id:
        :param progress:
        :return:
        """
        bgm = db_session.query(Bangumis).filter(Bangumis.id == id).first()
        try:
            bgm.progress = int(progress)
            if int(progress) == bgm.total:
                bgm.finish = True
            db_session.commit()
            logger.info('更新番剧 【{}】 成功!'.format(bgm.title))
            return True
        except Exception as e:
            db_session.rollback()
            logger.error('更新番剧 【{}】 失败! {}'.format(bgm.title, e))
            return False


    @staticmethod
    def del_bangumi(db_session, id):
        """
        Del
        :param db_session:
        :param id:
        :return:
        """
        try:
            db_session.query(Bangumis).filter(Bangumis.id == id).delete()
            db_session.commit()
            logger.info('删除番剧 【{}】 成功!'.format(id))
            return True
        except Exception as e:
            db_session.rollback()
            logger.error('删除番剧 【{}】 失败! {}'.format(id, e))
            return False
