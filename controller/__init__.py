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
import uuid
import json
import logging
import functools
import tornado.web
from service.Session import Session
from tornado import gen
from config.conf.conf_db import cookies_config, session_keys
from config.config import DEBUG, ACCESS_ALLOW_ORIGIN, REQUEST_AUTH_HEADER, APP_REQUEST_AUTH_HEADER, APP_MAC_ADDRESS
from model.models import to_dict
from service.LogService import LogService
from extends.utils import sha1_encrypt, str2base64, get_random_str, gettimestamp


logger = logging.getLogger(__name__)

""" 
    验证思路:
    1、客户端请求登录 (发送邮箱和密码)
    2、服务器验证 (客户端传进来的邮箱和密码) 失败 : 返回密码错误 / 成功 : 返回 access Token (保存用户信息[7天]、保存 access token [7200])
    3、每次请求都携带 access token 在此装饰函数验证 (
        失败: 拦截请求 返回401 要求重新登陆
        成功: 更新 (延长) access token 的过期时间 并且 放行请求
    ) 
    虽然简陋
    不过够用了  外加后台消息监听 网站一登录 立马通知邮件、推送消息到手机APP
"""
def auth_required(func):

    @functools.wraps(func)
    @gen.coroutine
    def wrapper(self, *args, **kwargs):
        print('=========================检测=========================')
        if REQUEST_AUTH_HEADER in self.request.headers.keys():
            cache_user_info = yield self.get_current_user_info()
            if cache_user_info is None:
                logger.info('用户信息为空')
                self.error_return(401)
            else:
                ### 获取客户端提交上来的 Token
                auth_token = self.request.headers[REQUEST_AUTH_HEADER]
                #################################################################
                auth_permission = yield self.cache_manager.get(key=auth_token)
                if auth_permission is None:
                    logger.info('Access Token 已经过期')
                    self.error_return(401)
                else:
                    ### 如果权限存在  更新用户权限的过期时间
                    yield self.cache_manager.set(key=auth_token,
                                           value=auth_token,
                                           expire_time=session_keys['auth_token_expire_time']
                                           )
                    logger.info('权限检测通过!')
                    yield func(self, *args, **kwargs)
                #################################################################
        elif APP_REQUEST_AUTH_HEADER in self.request.headers.keys():
            ############移动端检测#####################################################
            ### 获取客户端提交上来的 Token
            auth_token = self.request.headers[APP_REQUEST_AUTH_HEADER]
            if auth_token != APP_MAC_ADDRESS:
                logger.info('设备未授权')
                self.error_return(401)
            else:
                ### 如果权限存在  更新用户权限的过期时间
                yield self.cache_manager.set(key=auth_token,
                                             value=auth_token,
                                             expire_time=session_keys['auth_token_expire_time']
                                             )
                logger.info('权限检测通过!')
                yield func(self, *args, **kwargs)
            ############移动端END#####################################################
        else:
            logger.info('请求头中没有 Token 标识')
            self.error_return(401)
    return wrapper


"""================================================================================"""
"""
    API 部分父类
    初始化服务、添加常用方法
"""


class BaseHandler(tornado.web.RequestHandler):

    def AccessToken(self):
        """
        生成AccessToken
        :return: 唯一的token
        """
        random_str = str(get_random_str())
        uu_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, '__mex__'))
        timestamp = str(gettimestamp())
        token_str = sha1_encrypt(random_str + uu_id + timestamp)
        return str2base64(token_str)

    def initialize(self):
        self.session = None
        self.db_session = None
        self.session_save_tag = False
        self.session_expire_time = session_keys['login_user_expire_time']  # 7*24*60*60秒
        self.thread_executor = self.application.thread_executor
        self.cache_manager = self.application.cache_manager
        self.message_manager = self.application.message_manager
        self.async_do = self.thread_executor.submit
        self.client_ip = self.request.remote_ip
        self.log = dict(operate='', content='', client='', client_ip='')


    @gen.coroutine
    def pushMessageToApp(self, content):
        """
        推送消息到app
        :param content:
        :return:
        """
        message = " {0} Ip: {1} ".format(content, self.client_ip)
        self.message_manager.push(message)

    @gen.coroutine
    def prepare(self):
        """
        自动调用
        :return:
        """
        yield self.init_session()

    @gen.coroutine
    def init_session(self):
        """
        初始化session
        :return:
        """
        if self.session is None:
            self.session = Session(self)
            yield self.session.init_fetch()

    @property
    def db(self):
        """
        自动调用
        :return:
        """
        if not self.db_session:
            self.db_session = self.application.db_pool()
        return self.db_session

    def set_default_headers(self):
        """
        跨域设置
        :return:
        """
        ### 本地开发使用
        ### self.set_header('Access-Control-Allow-Origin', ACCESS_ALLOW_ORIGIN)
        self.set_header('Access-Control-Allow-Credentials', 'true')
        self.set_header('Access-Control-Allow-Headers','Content-Type, X-Requested-With, Origin, No-Cache, Cache-Control, X-XsrfToken, X-AuthToken')
        if self.request.method == 'GET' or self.request.method == 'POST':
            self.set_header('Access-Control-Allow-Methods', 'GET, POST')
        else:
            self.set_header('Access-Control-Allow-Methods', 'GET, POST, PUT, OPTIONS, DELETE')
        self.set_header('Cache-Control', 30)

    def save_session(self):
        """
        手动保存
        :return:
        """
        self.session_save_tag = True
        self.session.generate_session_id()

    @gen.coroutine
    def get(self, *args, **kwargs):
        """
        重写 GET 方法
        拦截 GET 请求
        默认返回 404
        :param args:
        :param kwargs:
        :return:
        """
        self.error_return(404)


    @gen.coroutine
    def options(self, *args, **kwargs):
        """
        重写 Options 方法
        Options 方法请求直接放行 设置 xsrf_token 防止请求伪造
        :param args:
        :param kwargs:
        :return:
        """
        self.set_cookie(cookies_config['xsrf_token_key_name'], str(self.xsrf_token, encoding='UTF-8'))


    @gen.coroutine
    def get_current_user_info(self):
        """
        先获取用户的 access token
        然后获取用户信息
        :return:
        """
        result = yield self.cache_manager.get(key=session_keys['login_user'])
        if result:
            return json.loads(str(result, encoding='utf-8'))
        else:
            return None

    def save_login_user(self, user, authToken):
        """
        保存登录用户的信息 和 access Token
        :param user:
        :param authToken:
        :return:
        """
        save_user = to_dict(user)
        save_user.pop('user_pass')
        self.cache_manager.remove(key=session_keys['login_user'])
        self.cache_manager.set(key=session_keys['login_user'], value=json.dumps(save_user), expire_time=self.session_expire_time)
        self.cache_manager.set(key=authToken, value=authToken, expire_time=session_keys['auth_token_expire_time'])

    @gen.coroutine
    def save_log(self, action, content):
        """
        添加用户操作日志
        这里用 Handler 传过来的 db_session 对象会出错
        重新获取一个 db_session 对象
        然后手动关闭
        :param action: 用户操作
        :param content: 操作详情
        :return:
        """
        self.log['operate'] = action
        self.log['content'] = content
        self.log['client'] = ''
        self.log['client_ip'] = self.client_ip
        db_session = self.application.db_pool()
        yield self.async_do(LogService.add_log, db_session, self.log)
        db_session.close()

    def get_all_argument(self):
        """
        前端用 axios 传过来的参数 tornado 获取不到
        获取全部输入参数
        :return:
        """
        data = self.request.body
        return json.loads(data)

    def to_dict(self, data):
        """
        将 SqlAlchemy 查询的数据转成字典格式
        :param data:
        :return:
        """
        return to_dict(data)

    def json_return(self, data):
        """
        返回json数据
        :param data: 数据字典
        :return:
        """
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.set_cookie(cookies_config['xsrf_token_key_name'], str(self.xsrf_token, encoding='UTF-8'))
        logger.info('客户端IP : {0}'.format(self.client_ip))
        if self.request.method != 'GET':
            data['client_ip'] = str(self.client_ip)
        self.write(json.dumps(data))

    def write_error(self, status_code, **kwargs):
        """
        重写错误输出
        拦截tornado异常
        :param status_code:
        :param kwargs:
        :return:
        """
        self.error_return(status_code)

    def error_return(self, code, message=None):
        """
        公用错误返回
        :param code: 状态码
        :param message: 可选 用于 handler 中主动返回错误
        :return:
        """
        self.set_status(code)
        if code == 400:
            self.json_return({'error': '投喂参数出错了 ~ ', 'meg': message})
        elif code == 401:
            self.json_return({'error': '你没有权限!', 'meg': message})
        elif code == 403:
            self.json_return({'error': '禁止访问', 'meg': message})
        elif code == 404:
            self.json_return({'error': '该资源从地球上消失了 ~ ', 'meg': message})
        elif code == 405:
            self.json_return({'error': '请求错误', 'meg': message})
        elif code == 500:
            self.json_return({'error': '服务器抽风了 ~ ', 'meg': message})
        else:
            self.json_return({'error': '{0} 未知错误'.format(code)})

    @gen.coroutine
    def on_finish(self):
        """
        tornado 自动调用
        关闭数据库连接
        :return:
        """
        if self.db_session:
            self.db_session.close()
        if self.session is not None and self.session_save_tag:
            yield self.session.save(self.session_expire_time)
