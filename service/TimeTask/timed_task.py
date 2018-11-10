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
import os
import time
import logging
from config.conf.conf_db import db_config
from extends.qiniu import Qiniu
from .TimedTaskService import TimeTask

logger = logging.getLogger(__name__)

'''
    定时任务 初始化
    这里添加要定时执行的任务
'''


def time_task_backup_db():
    """
    备份数据库
    本地备份的数据库存在 db_back_path 目录下
    并把数据库文件上传到七牛云私有空间
    :return:
    """
    backup_sql_path = '/var/lib/mysql' + os.sep + 'backups_' + db_config['dbname'] + '_' + time.strftime("%Y%m%d%H%M%S", time.localtime(int(time.time())))
    cmd = 'docker exec -it mysql bash mysqldump --user={0} --password={1} --skip-lock-tables {2} > {3}'.format(db_config['user'], db_config['password'], db_config['dbname'],backup_sql_path)
    result = os.system(cmd)
    if result != 0:
        logger.error('定时任务 数据库备份 : 备份数据库失败')
    else:
        backup_sql_path = backup_sql_path.replace('/var/lib/mysql', '/www/docker/mysql/data')
        if os.path.isfile(backup_sql_path):
            # 将备份的数据库文件推送到七牛云
            try:
                qiniu = Qiniu()
                qiniu.put_backup(backup_sql_path)
                logger.info('定时任务 数据库备份 上传备份文件到七牛云 成功！')
            except Exception as e:
                logger.error('定时任务 数据库备份 上传备份文件到七牛云 失败！ {0}'.format(e))
    logger.info('定时任务 数据库备份 执行完毕')



def time_task_start_japonx_spider():
    """
    启动爬虫
    :return:
    """
    commend = 'cd {} && chmod +x start.sh && ./start.sh'.format(os.path.join(os.getcwd(), 'spider'))
    try:
        os.system(commend)
        logger.info('定时任务 启动爬虫 启动成功')
    except Exception as e:
        logger.error('定时任务 启动爬虫 Error  {}'.format(e))



#####################################################################################
### 初始化定时任务
#####################################################################################
def init_task():
    timeTask = TimeTask()
    try:
        # 添加任务
        timeTask.add_task(func=time_task_backup_db, day_of_week='sun') # 备份数据库
        timeTask.add_task(func=time_task_start_japonx_spider, mode="interval", days=3)  # 启动爬虫
        # 启动任务调度
        timeTask.start_tasks()
        logger.info('初始化定时任务 成功!')
    except Exception as e:
        logger.error('初始化定时任务 失败! {0}'.format(e))
