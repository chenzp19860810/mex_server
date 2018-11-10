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
from model.models import Logs

logger = logging.getLogger(__name__)

'''
    后台用户日常操作
'''


class LogService:

    ### 获取日志列表
    @staticmethod
    def log_list(db_session, pager, count=None):
        query = db_session.query(Logs)
        return BaseService.query_pager(query=query,pager=pager, count=count)


    ### 添加日志
    @staticmethod
    def add_log(db_session, logInfo):
        try:
            log = Logs()
            log.operate = logInfo['operate']  # 操作类型
            log.content = logInfo['content']  # 操作详情
            log.client = logInfo['client']  # 客户端信息
            log.client_ip = logInfo['client_ip']  # 客户端 IP
            db_session.add(log)
            db_session.commit()
            logger.info('添加日志成功')
        except Exception as e:
            db_session.rollback()
            logger.error('添加日志失败  {0}'.format(e))


    ### 清空全部日志
    @staticmethod
    def clearLogs(db_session, ip):
        log = {}
        log['operate'] = '清空日志'
        log['client'] = ''
        log['client_ip'] = ip
        query = db_session.query(Logs)
        try:
            query.filter(Logs.id > 0).delete(synchronize_session=False)
            db_session.commit()
            log['content'] = '清空日志成功'
            LogService.add_log(db_session, log)
            logger.info('清空日志成功')
            return True
        except Exception as e:
            db_session.rollback()
            log['content'] = '清空日志失败'
            LogService.add_log(db_session, log)
            logger.error('清空日志失败  {0}'.format(e))
            return False