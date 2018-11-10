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
from model.models import Users

logger = logging.getLogger(__name__)

class UserService:

    @staticmethod
    def query_user(db_session,pager=None, count=None, user_email=None):
        """
        查询用户信息
        :param db_session: 数据库对象
        :param pager: 分页对象
        :param count:
        :param user_email: 用户邮箱
        :return:
        """
        if user_email is None:
            query = db_session.query(Users).filter(Users.user_group != 'administrator').all()
            return BaseService.query_pager(query, pager, count)
        else:
            return db_session.query(Users).filter(Users.user_email == user_email).first()


    @staticmethod
    def add_user(db_session, data):
        user = Users(
            user_email=data['email'],
            user_pass=data['password'],
            user_nickname=data['nickname'],
            user_url=data['url']
        )

    @staticmethod
    def rest_pass(db_session, data):
        administrator = db_session.query(Users).filter(Users.user_group == 'administrator').first()
        if administrator.verify_password(data['oldpass']):
            try:
                administrator.reset_password(data['newpass'].strip())
                db_session.commit()
                logger.info('更改管理员密码成功')
                return True
            except Exception as e:
                db_session.rollback()
                logger.error('更改管理员密码失败  {}'.format(e))
                return False
        else:
            return False

    @staticmethod
    def update_admin_info(db_session, data):
        user = db_session.query(Users).filter(Users.user_group == 'administrator').order_by(Users.user_register_at.asc()).first()
        if user:
            user.user_email = data['email']
            user.user_avatar = data['avatar']
            user.user_nickname = data['nickname']
            user.user_introduction = data['description']
            try:
                db_session.commit()
                logger.info('更改管理员信息成功')
                return True
            except Exception as e:
                db_session.rollback()
                logger.error('更改管理员信息失败  {}'.format(e))
                return False
        else:
            return False