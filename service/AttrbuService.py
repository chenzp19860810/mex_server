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
from model.models import Attributes

logger = logging.getLogger(__name__)


class CategoryService:


    @staticmethod
    def category(db_session, arg):
        if arg.isdigit():
            return db_session.query(Attributes).filter(Attributes.type == 'category', Attributes.id == arg).first()
        else:
            return db_session.query(Attributes).filter(Attributes.type == 'category', Attributes.slug == arg).first()


    @staticmethod
    def category_list(db_session,pager, count=None):
        query = db_session.query(Attributes.id, Attributes.name, Attributes.slug, Attributes.poster, Attributes.description).filter(Attributes.type == 'category').distinct()
        return BaseService.query_pager(query, pager, count)

    @staticmethod
    def add_category(db_session, data):
        result = {}
        try:
            count = db_session.query(Attributes).filter(Attributes.name == data['name'], Attributes.type == 'category').count()
            if count > 0:
                result['state'] = False
                result['message'] = '分类已经存在，不能重复添加'
            else:
                cate = Attributes()
                cate.name = str(data['name'].strip())
                cate.slug = str(data['slug'].strip())
                cate.description = str(data['description'].strip())
                cate.poster = str(data['poster'].strip())
                cate.type = 'category'
                db_session.add(cate)
                db_session.commit()
                logger.info('添加分类 {0} 成功'.format(data['name']))
                result['state'] = True
                result['message'] = '添加分类成功'
        except Exception as e:
            db_session.rollback()
            logger.error('添加分类 {0} 失败  {1}'.format(data['name'], e))
            result['state'] = False
            result['message'] = '添加分类失败'
        finally:
            return result


    @staticmethod
    def update(db_session, id ,data):
        try:
            result = db_session.query(Attributes).filter(Attributes.id == id, Attributes.type=='category').first()
            result.name = data['name']
            result.slug = data['slug']
            result.description = data['description']
            result.poster = data['poster']
            db_session.commit()
            logger.info('更新分类 【{0}】 成功!'.format(id))
            return True
        except Exception as e:
            logger.error('更新分类 【{0}】 失败!  {1}'.format(id, e))
            db_session.rollback()
            return False


    @staticmethod
    def del_category(db_session, id):
        try:
            db_session.query(Attributes).filter(Attributes.id == id, Attributes.type == 'category').delete()
            db_session.commit()
            logger.info('删除分类 【{0}】 成功!'.format(id))
            return True
        except Exception as e:
            db_session.rollback()
            logger.error('删除分类 【{0}】 失败!'.format(id))
            return False

'''
    tag 的操作
'''

class TagService:

    ### 添加新标签
    @staticmethod
    def tag_list(db_session, pager, count=None):
        query = db_session.query(Attributes.id, Attributes.name).filter(Attributes.type == 'tag')
        return BaseService.query_pager(query,pager,count)

    ### 添加新标签
    @staticmethod
    def add_tag(db_session, tagName):
        result = {}
        try:
            count = db_session.query(Attributes).filter(Attributes.name == tagName, Attributes.type == 'tag').count()
            if count > 0:
                result['state'] = False
                result['message'] = '标签已经存在，不能重复添加'
            else:
                tag = Attributes()
                tag.name = str(tagName)
                tag.slug = str(tagName)
                tag.type = 'tag'
                db_session.add(tag)
                db_session.commit()
                logger.info('添加新标签 {0} 成功'.format(tagName))
                result['state'] = True
                result['message'] = '添加标签成功'
        except Exception as e:
            db_session.rollback()
            logger.info('添加新标签 {0} 失败  {1}'.format(tagName, e))
            result['state'] = False
            result['message'] = '添加标签失败'
        finally:
            return result

    @staticmethod
    def del_tag(db_session, tagName = None):
        query = db_session.query(Attributes)
        if tagName:
            ### 删除单个标签
            tag = query.filter(Attributes.name == tagName, Attributes.type == 'tag').first()
            try:
                if tag:
                    db_session.delete(tag)
                    db_session.commit()
                logger.info('删除标签成功')
                return True
            except Exception as e:
                logger.info('删除标签失败  {0}'.format(e))
                return False
        else:
            ### 删除全部标签
            try:
                query.filter(Attributes.id > 0, Attributes.type == 'tag').delete(synchronize_session=False)
                db_session.commit()
                logger.info('删除全部标签成功')
                return True
            except Exception as e:
                db_session.rollback()
                logger.info('删除全部标签失败 {0}'.format(e))
                return False


