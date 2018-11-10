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

"""
    后台相关设置
    添加常用查询接口
    本服务下全部内容使用缓存

"""

import json
import logging
from model.models import Menus,Options, to_dict

logger = logging.getLogger(__name__)


class OptionsService:

    @staticmethod
    def query_options(db_session, options_name):
        data = db_session.query(Options).filter(Options.option_name == options_name).first()
        if data:
            if data.option_value:
                return json.loads(data.option_value)
            else:
                return None
        else:
            return None

    @staticmethod
    def add_options(db_session, options_name, options_value):
        options = Options(
            option_name=options_name,
            option_value=json.dumps(options_value)
        )
        try:
            db_session.add(options)
            db_session.commit()
            logger.info('添加设置成功')
            return True
        except Exception as e:
            db_session.rollback()
            logger.error('添加设置失败 {}'.format(e))
            return False

    @staticmethod
    def update_options(db_session, options_name, options_value):
        options = db_session.query(Options).filter(Options.option_name == options_name).first()
        if options:
            try:
                options.option_value = json.dumps(options_value)
                db_session.commit()
                logger.info('更新设置成功')
                return True
            except Exception as e:
                db_session.rollback()
                logger.error('更新配置失败 {}'.format(e))
                return False
        else:
            return False

    @staticmethod
    def del_options(db_session, options_name):
        db_session.query(Options).filter(Options.option_name == options_name).delete()
        try:
            db_session.commit()
            logger.info('删除配置成功')
            return True
        except Exception as e:
            db_session.rollback()
            logger.error('删除配置失败 {}'.format(e))
            return False


class MenusService:

    @staticmethod
    def query_menus(db_session, id=None, returnList='tree'):
        if id is None:
            if returnList == 'tree':
                menus = []
                parent = db_session.query(Menus).filter(Menus.parent_id == 0).order_by(Menus.order.asc()).all()
                for item in parent:
                    children = db_session.query(Menus).filter(Menus.parent_id == item.id).order_by(Menus.order.asc()).all()
                    menu = to_dict(item)
                    if children:
                        menu['children'] = to_dict(children)
                    else:
                        menu['children'] = None
                    menus.append(menu)

                return {
                    'list': menus
                }
            else:
                menus = []
                parent = db_session.query(Menus).filter(Menus.parent_id == 0).order_by(Menus.order.asc()).all()
                for item in parent:
                    menus.append(to_dict(item))
                    children = db_session.query(Menus).filter(Menus.parent_id == item.id).order_by(Menus.order.asc()).all()
                    if children:
                        for ch in children:
                            ch.name = '|------- ' + ch.name
                            menus.append(to_dict(ch))

                return {
                    'list': menus
                }
        else:
            return db_session.query(Menus).filter(Menus.id == id).first()


    @staticmethod
    def add_menus(db_session, data):
        menu = Menus(
            name=data['name'].strip(),
            iconCls=data['iconCls'].strip(),
            link=data['link'].strip(),
            order=data['order'],
            parent_id=data['parent_id']
        )

        try:
            db_session.add(menu)
            db_session.commit()
            logger.info('添加菜单 【{}】 成功'.format(data['name']))
            return True
        except Exception as e:
            db_session.rollback()
            logger.error('添加菜单 【{}】 失败  {}'.format(data['name'], e))
            return False


    @staticmethod
    def update_menus(db_session, id, data):
        menu = db_session.query(Menus).filter(Menus.id == id).first()
        if menu:
            menu.name = data['name']
            menu.iconCls = data['iconCls']
            menu.link = data['link']
            menu.order = data['order']
            menu.parent_id = data['parent_id']
            try:
                db_session.commit()
                logger.info('更新菜单 【{}】 成功'.format(data['name']))
                return True
            except Exception as e:
                db_session.rollback()
                logger.error('更新菜单 【{}】 失败 {}'.format(data['name'], e))
                return False
        else:
            logger.error('菜单不存在')
            return False


    @staticmethod
    def del_menus(db_session, id):
        try:
            db_session.query(Menus).filter(Menus.id == id).delete()
            db_session.commit()
            logger.info('删除菜单成功')
            return True
        except Exception as e:
            db_session.rollback()
            logger.error('删除菜单成功  {}'.format(e))
            return False