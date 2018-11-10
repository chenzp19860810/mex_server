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
import json
import logging
from . import BaseService
from extends.utils import gettimestamp
from model.models import Posts, Attributes

logger = logging.getLogger(__name__)

class ArticleService:


    @staticmethod
    def home_article_list(db_session, pager, where=None):
        query = db_session.query(Posts.id,
                                 Posts.post_title,
                                 Posts.post_poster,
                                 Posts.comment_status,
                                 Posts.post_markdown,
                                 Posts.created_at,
                                 Posts.comment_count,
                                 Posts.top,
                                 Posts.like_count,
                                 Posts.view_count,
                                 Attributes.slug,
                                 Attributes.poster,
                                 Attributes.name).join(Attributes).filter(Posts.post_status == 'publish', Posts.post_openness == 'public').order_by(Posts.created_at.desc())
        if where is not None:
            query = query.filter(Attributes.slug == where.strip())

        return BaseService.query_pager(query, pager, None)

    @staticmethod
    def article_list(db_session, pager, count=None, where=None):
        """
        列表
        :param db_session:
        :param pager:
        :param count:
        :return:
        """
        query = db_session.query(Posts.id,
                                 Posts.post_title,
                                 Posts.post_poster,
                                 Posts.post_openness,
                                 Posts.post_status,
                                 Posts.comment_status,
                                 Attributes.slug,
                                 Attributes.name).join(Attributes).order_by(Posts.created_at.desc())
        if where is not None:
            if where != 'all':
                query = query.filter(Posts.post_status == where)
        return BaseService.query_pager(query, pager, count)


    @staticmethod
    def query_article(db_session, id):
        """
        :param db_session:
        :param id:
        :return:
        """
        return db_session.query(
                                 Posts.id,
                                 Posts.post_title,
                                 Posts.post_poster,
                                 Posts.post_markdown,
                                 Posts.comment_status,
                                 Posts.created_at,
                                 Posts.update_at,
                                 Posts.post_openness,
                                 Posts.comment_count,
                                 Posts.category_id,
                                 Posts.top,
                                 Posts.tags,
                                 Posts.like_count,
                                 Posts.view_count,
                                 Attributes.slug,
                                 Attributes.name).join(Attributes).filter(Posts.id == id).first()


    @staticmethod
    def add_article(db_session, data):
        """
        添加
        :param db_session:
        :param data:
        :return:
        """
        article = Posts()
        article.post_title = data['post_title'].strip()
        article.post_poster = data['post_poster'].strip()
        article.post_markdown = data['post_markdown']
        article.post_status = data['post_status'].strip()
        article.post_openness = data['post_openness'].strip()
        article.created_at = int(int(data['created_at']) / 1000) if len(str(data['created_at'])) == 13 else int(data['created_at'])
        article.category_id = int(data['category_id'])
        article.tags = json.dumps(data['tags'])
        article.top = data['top']
        article.comment_status = data['comment_status']
        try:
            db_session.add(article)
            db_session.commit()
            logger.info('添加文章 【{}】 成功!'.format(data['post_title']))
            return article.id
        except Exception as e:
            db_session.rollback()
            logger.error('添加文章 【{0}】 失败! {1}'.format(data['post_title'], e))
            return False


    @staticmethod
    def update_article_views(db_session, id):
        try:
            article = db_session.query(Posts).filter(Posts.id == id, Posts.post_status == 'publish', Posts.post_openness == 'public').first()
            if article is not None:
                oldView = article.view_count
                article.view_count = int(oldView + 1)
                logger.info('更新文章文章浏览数 【{}】 成功!'.format(id))
                db_session.commit()
            else:
                return True
        except Exception as e:
            db_session.rollback()
            logger.error('更新文章文章浏览数 【{0}】 失败! {1}'.format(id, e))
            return False



    @staticmethod
    def update_article(db_session, id, data=None):
        if data is None:
            article = db_session.query(Posts).filter(Posts.id == id).first()
            article.post_status = 'publish'
            try:
                db_session.commit()
                logger.info('还原文章 【{}】 成功!'.format(article.post_title))
                return True
            except Exception as e:
                logger.error('还原文章 【{0}】 失败! {1}'.format(article.post_title, e))
                db_session.rollback()
                return False
        else:
            article = db_session.query(Posts).filter(Posts.id == id).first()
            article.post_title = data['post_title'].strip()
            article.post_poster = data['post_poster'].strip()
            article.post_markdown = data['post_markdown']
            article.post_openness = data['post_openness'].strip()
            article.created_at = int(int(data['created_at']) / 1000) if len(str(data['created_at'])) == 13 else int(
                data['created_at'])
            article.update_at = gettimestamp()
            article.category_id = int(data['category_id'])
            article.tags = json.dumps(data['tags'])
            article.top = data['top']
            article.comment_status = data['comment_status']
            try:
                db_session.commit()
                logger.info('更新文章 【{}】 成功!'.format(data['post_title']))
                return True
            except Exception as e:
                logger.error('更新文章 【{0}】 失败! {1}'.format(data['post_title'], e))
                db_session.rollback()
                return False

    @staticmethod
    def remove_article(db_session, articleId):
        """
        将文章移动到回收站
        :param db_session:
        :param articleId:
        :return:
        """
        article = db_session.query(Posts).filter(Posts.id == articleId).first()
        try:
            article.post_status = 'recovery'
            db_session.commit()
            logger.info('文章移动到回收站 【{}】 成功!'.format(articleId))
            return True
        except Exception as e:
            db_session.rollback()
            logger.error('文章移动到回收站 【{0}】 失败! {1}'.format(articleId, e))
            return False

    @staticmethod
    def del_article(db_session, articleId):
        """
        将文章移动到回收站
        :param db_session:
        :param articleId:
        :return:
        """
        db_session.query(Posts).filter(Posts.id == articleId).delete()
        try:
            db_session.commit()
            logger.info('删除文章 【{}】 成功!'.format(articleId))
            return True
        except Exception as e:
            db_session.rollback()
            logger.error('删除文章 【{0}】 失败! {1}'.format(articleId, e))
            return False