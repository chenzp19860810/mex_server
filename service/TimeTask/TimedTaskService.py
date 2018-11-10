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
from config.conf.conf_db import engine_url
from apscheduler.schedulers.tornado import TornadoScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

logger = logging.getLogger(__name__)

'''
    定时任务  常用配置参数
    
    [ cron ] 定时调度（某一定时时刻执行）
    (int|str) 表示参数既可以是int类型，也可以是str类型
    (datetime | str) 表示参数既可以是datetime类型，也可以是str类型
    year (int|str) – 4-digit year -（表示四位数的年份，如2008年）
    month (int|str) – month (1-12) -（表示取值范围为1-12月）
    day (int|str) – day of the (1-31) -（表示取值范围为1-31日）
    week (int|str) – ISO week (1-53) -（格里历2006年12月31日可以写成2006年-W52-7（扩展形式）或2006W527（紧凑形式））
    day_of_week (int|str) – number or name of weekday (0-6 or mon,tue,wed,thu,fri,sat,sun) - （表示一周中的第几天，既可以用0-6表示也可以用其英语缩写表示）
    hour (int|str) – hour (0-23) - （表示取值范围为0-23时）
    minute (int|str) – minute (0-59) - （表示取值范围为0-59分）
    second (int|str) – second (0-59) - （表示取值范围为0-59秒）
    start_date (datetime|str) – earliest possible date/time to trigger on (inclusive) - （表示开始时间）
    end_date (datetime|str) – latest possible date/time to trigger on (inclusive) - （表示结束时间）
    timezone (datetime.tzinfo|str) – time zone to use for the date/time calculations (defaults to scheduler timezone) -（表示时区取值）
    
    [ interval ] 间隔调度（每隔多久执行）
    weeks (int) – number of weeks to wait
    days (int) – number of days to wait
    hours (int) – number of hours to wait
    minutes (int) – number of minutes to wait
    seconds (int) – number of seconds to wait
    start_date (datetime|str) – starting point for the interval calculation
    end_date (datetime|str) – latest possible date/time to trigger on
    timezone (datetime.tzinfo|str) – time zone to use for the date/time calculations
    
    [ date ] 定时调度（作业只会执行一次）
    run_date (datetime|str) – the date/time to run the job at  -（任务开始的时间）
    timezone (datetime.tzinfo|str) – time zone for run_date if it doesn’t have one already
'''

class TimeTask:

    def __init__(self):
        self.scheduler = TornadoScheduler()
        # 存储器 默认使用sql数据库
        mysql_store = SQLAlchemyJobStore(url=engine_url, tablename='mex_apscheduler_jobs')
        self.scheduler.add_jobstore(mysql_store)
        ### 可以自定义更改 使用redis
        ### redis_store = RedisJobStore(host=redis_config['host'], port=redis_config['port'])
        ### self.scheduler.add_jobstore(redis_store, alias='redis')

    # 添加定时任务
    def add_task(self, func, mode='cron', *args, **kwargs):
        self.scheduler.add_job(func, trigger=mode, *args, **kwargs, replace_existing=True, max_instances=1)
        return self

    # 启动定时任务
    def start_tasks(self):
        self.scheduler.start()
