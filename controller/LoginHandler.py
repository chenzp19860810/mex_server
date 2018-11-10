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
from tornado import gen
from controller import BaseHandler, auth_required
from extends.utils import base642str
from config.conf.conf_db import cookies_config, session_keys
from extends.utils import gettimestamp
from config.config import GEETEST, REQUEST_AUTH_HEADER
from extends.geetest.geetest import GeetestLib
from service.UserService import UserService


logger = logging.getLogger(__name__)

'''
    用户登录 权限认证
'''
class LoginHnadler(BaseHandler):

    @auth_required
    @gen.coroutine
    def get(self, *args, **kwargs):
        user_info = yield self.get_current_user_info()
        if user_info is None:
            self.error_return(401)
        else:
            self.json_return({
                'code': 0,
                'data': user_info
            })

    @gen.coroutine
    def post(self, action, **kwargs):
        self.set_status(201)
        if action == 'login':
            yield self.user_login()
        else:
            self.error_return(403)

    # 登录
    @gen.coroutine
    def user_login(self):
        """
            用户登录
        :return:
        """
        data = self.get_all_argument()
        input_user_email = data['loginame'].strip() if 'loginame' in data.keys() else None
        input_user_pass = data['password'].strip() if 'password' in data.keys() else None
        input_user_remember = data['remember'] if 'remember' in data.keys() else False

        if input_user_email and input_user_pass:
            ### 解码后的用户邮箱 和 密码
            user_email = base642str(input_user_email).lower()
            user_pass = base642str(input_user_pass)
            ### 检测用户名、密码是否正确
            user = yield self.async_do(UserService.query_user, self.db, user_email=user_email.lower())
            if user:
                if user.verify_password(user_pass):
                    if input_user_remember:
                        self.set_cookie(cookies_config['remember_login'], input_user_email)
                        self.set_cookie(cookies_config['remember_pass'], input_user_pass)
                    else:
                        self.clear_cookie(cookies_config['remember_login'])
                        self.clear_cookie(cookies_config['remember_pass'])

                    ### 保存日志
                    self.save_log("用户登录", "用户登录成功")
                    ### 推送消息到APP
                    self.pushMessageToApp("用户登录成功")
                    accessToken = self.AccessToken()
                    self.save_login_user(user, accessToken)

                    self.json_return({
                        'code': 0,
                        'data':{
                            'token': accessToken
                        }
                    })
                else:
                    ### 保存日志
                    self.save_log("用户登录", "用户登录失败[密码错误]")
                    ### 推送消息到APP
                    self.pushMessageToApp("用户登录失败[密码错误]")
                    self.json_return({
                        'code': 9901,
                        'error': '密码错误'
                    })
            else:
                ### 保存日志
                self.save_log("用户登录", "用户登录失败[用户名错误]")
                ### 推送消息到APP
                self.pushMessageToApp("用户登录失败[用户名错误]")
                self.json_return({
                    'code': 9901,
                    'error': '用户名错误'
                })
        else:
            self.error_return(400)


    @gen.coroutine
    def delete(self, *args, **kwargs):
        """
        退出
        :param args:
        :param kwargs:
        :return:
        """
        if REQUEST_AUTH_HEADER in self.request.headers.keys():
            auth_token = self.request.headers['X-AuthToken']
            if auth_token:
                self.cache_manager.remove(key=auth_token)
        self.cache_manager.remove(key=session_keys['login_user'])
        self.json_return({
            'code': 0,
            'msg': 'Success!'
        })




'''
    极验 验证
'''
class GetCaptchaHandler(BaseHandler):

    @gen.coroutine
    def get(self, *args, **kwargs):
        """
        极验验证
        :param args:
        :param kwargs:
        :return:
        """
        user_id = '__mex_{0}__'.format(gettimestamp())
        geetest = GeetestLib(GEETEST['geetest_id'], GEETEST['geetest_key'])
        status = geetest.pre_process(user_id, JSON_FORMAT=0,ip_address="127.0.0.1")
        if status:
            status = 2
        self.session[geetest.GT_STATUS_SESSION_KEY] = status
        self.session['user_id'] = user_id
        self.save_session()
        response = geetest.get_response_str()
        responseDict = json.loads(response)
        responseDict['product'] = GEETEST['product']
        self.set_status(200)
        data = {
            'code':0,
            'data': responseDict
        }
        self.json_return(data)

class ValidateHandler(BaseHandler):

    @gen.coroutine
    def post(self, *args, **kwargs):
        geetest = GeetestLib(GEETEST['geetest_id'], GEETEST['geetest_key'])
        challenge = self.get_argument(geetest.FN_CHALLENGE, "")
        validate = self.get_argument(geetest.FN_VALIDATE, "")
        seccode = self.get_argument(geetest.FN_SECCODE, "")
        status = self.session[geetest.GT_STATUS_SESSION_KEY]
        user_id = self.session["user_id"]
        if status == 1:
            result = geetest.success_validate(challenge, validate, seccode, user_id, JSON_FORMAT=0)
        else:
            result = geetest.failback_validate(challenge, validate, seccode)
            self.session["user_id"] = user_id
            self.save_session()
        result_code = 0 if result else 999
        self.json_return({
            'code': result_code
        })

