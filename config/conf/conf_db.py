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
import pymysql
from config.config import DEBUG, DATABASE
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

pymysql.install_as_MySQLdb()

# cookies 设置
cookies_config = dict(
    xsrf_token_key_name='__mex_pct__',
    remember_login='__mex_lg__',
    remember_pass='__mex_pw__',
    session_key_name='__mex__'
)

# session key 映射
session_keys = dict(
    auth_token_key_name='mex_access_token',
    auth_token_expire_time=3600,  ### 后台 api 接口同肯过期时间(秒) access token 一个小时后失效
    login_user_token_key='login_user_token',
    login_user="login_user",
    login_user_expire_time=604800 ### 用户信息缓存时间
)

# redis 缓存 key 映射 (后面跟上内容ID)
redis_cache_keys = dict(
    cache_options_key = '__mex_options__',              ### 缓存配置
    cache_menus_key = '__mex_menus__',                  ### 缓存导航栏菜单
    cache_article_key = '__mex_article_{}__',           ### 缓存全部文章 单篇缓存
    cache_article_pages_key = '__mex_article_page_{}__', ### 缓存分页
    cache_article_views_key = '__mex_article_views_'    ### 文章访问量   先缓存 定时更新缓存
)

# 缓存服务器配置(redis)
redis_config = dict(
    host=DATABASE['redis_host'],
    port=DATABASE['redis_port'],
    password=None,
    max_connections=500,
    session_key_name=cookies_config['session_key_name'],
    session_expires_days=3  # cookies 过期天数
)

# 存储数据库配置 (mysql)
db_config = dict(
    host=DATABASE['mysql_host'],
    port=DATABASE['mysql_port'],
    user=DATABASE['mysql_user'],
    password=DATABASE['mysql_password'],
    dbname=DATABASE['mysql_dbname'],
    charset='utf8'
)

#############################################################################
#############################################################################
#############################################################################

### 连接字符串
engine_url = 'mysql+mysqldb://{0}:{1}@{2}:{3}/{4}?charset={5}'.format(db_config['user'], db_config['password'],
                                                                      db_config['host'], db_config['port'],
                                                                      db_config['dbname'], db_config['charset'])

### 配置
engine_setting = dict(
    ### 输出 sql
    echo=DEBUG,
    echo_pool=DEBUG,
    ### 设置一小时后回收连接池，默认-1，从不重置
    pool_recycle=3600,
    ### 连接池大小
    pool_size=100,
    ### 超过连接池大小外最多创建的连接
    max_overflow=30,
    encoding="utf-8"
)


### 初始化连接
def init_db_pool():
    engine = create_engine(engine_url, **engine_setting)
    db_pool_session = sessionmaker(bind=engine)
    return db_pool_session
