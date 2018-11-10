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
from model.models import Links

logger = logging.getLogger(__name__)

class FuncService:


    @staticmethod
    def query_link(db_session, pager=None, count=None, link_id=None):
        if link_id is None:
            # 查询链接列表
            query = db_session.query(Links)
            return BaseService.query_pager(query, pager, count)
        else:
            return db_session.query(Links).filter(Links.id == link_id).first()

    @staticmethod
    def add_link(db_session, data):
        link = Links(
            name=data['name'].strip(),
            poster=data['poster'].strip(),
            link=data['link'].strip(),
            description=data['description'].strip()
        )
        try:
            db_session.add(link)
            db_session.commit()
            logger.info('添加链接成功')
            return True
        except Exception as e:
            db_session.rollback()
            logger.error('添加链接失败 {}'.format(e))
            return False

    @staticmethod
    def update_link(db_session, id, data):
        link = db_session.query(Links).filter(Links.id == id).first()
        link.name = data['name'].strip()
        link.link = data['link'].strip()
        link.poster = data['poster'].strip()
        link.description = data['description'].strip()
        try:
            db_session.commit()
            logger.info('更新成功')
            return True
        except Exception as e:
            db_session.rollback()
            logger.error('更新失败')
            return False

    @staticmethod
    def del_link(db_session, id):
        try:
            db_session.query(Links).filter(Links.id == id).delete()
            db_session.commit()
            logger.info('删除成功')
            return True
        except Exception as e:
            db_session.rollback()
            logger.error('删除失败 {}'.format(e))
            return False