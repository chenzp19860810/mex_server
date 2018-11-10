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

'''
    常用、易变动的全局配置项
    将 易变动 的配置独立出来
    方便后期维护  不用到处翻
'''

### 运行模式
DEBUG = True

### 数据库配置
DATABASE = dict(
    mysql_host='127.0.0.1',
    mysql_port=3306,
    mysql_user='root',
    mysql_password='',
    mysql_dbname='',

    redis_host="127.0.0.1",
    redis_port=6379
)


REQUEST_AUTH_HEADER = 'X-AuthToken' # web 请求头
APP_REQUEST_AUTH_HEADER = 'APP-AuthToken'  # app 请求头
### 移动端 MAC 地址
APP_MAC_ADDRESS = ""

### 跨域设置
### 域名/IP + 端口号
ACCESS_ALLOW_ORIGIN = ""

### 极验 api 配置
GEETEST = dict(
    product = '',       # 验证形式 float, popup, bind
    geetest_id = '',
    geetest_key = ''
)

### 七牛云 配置
QINIU = dict(
    access_key = '',
    secret_key = '',
    public_bucket_name = '',           # 公共存储空间名称  用于存放图片
    private_bucket_name = '',      # 私有存储空间名称  用于存放备份文件
    image_policy = ''  # 七牛图片处理接口
)

### MobPush配置
MOBPUSH = dict(
    AppKey = '',
    AppSecret = ''
)