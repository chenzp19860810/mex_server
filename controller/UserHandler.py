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
from . import BaseHandler, auth_required
from model.models import Users
from tornado import gen
from service.UserService import UserService

class UserHandler(BaseHandler):

    @gen.coroutine
    def get(self, userId=None, **kwargs):
        print(userId)
        if userId:
            userInfo = self.db.query(Users.id,
                                     Users.user_email,
                                     Users.user_nickname,
                                     Users.user_avatar,
                                     Users.user_url,
                                     Users.user_introduction,
                                     Users.user_register_at,
                                     Users.user_status,
                                     Users.user_group
                                     ).filter(Users.id == userId).first()
            if userInfo:
                self.json_return({
                    'code': 0,
                    'data': self.to_dict(userInfo)
                })
            else:
                self.json_return({
                    'code': 9904,
                    'error': '用户不存在~'
                })
        else:
            self.error_return(400)


    @auth_required
    @gen.coroutine
    def post(self, *args, **kwargs):
        pass


    @auth_required
    @gen.coroutine
    def put(self, arg=None, **kwargs):
        if isinstance(arg, str):
            data = self.get_all_argument()
            if arg == 'resetPass':
                result = yield self.async_do(UserService.rest_pass, self.db, data)
                if result:
                    self.json_return({
                        'code':0,
                        'msg':'更改管理员密码成功'
                    })
                else:
                    self.json_return({
                        'code': 9901,
                        'error': '更改管理员密码失败'
                    })
            elif arg == 'info':
                ### 更改信息
                result = yield self.async_do(UserService.update_admin_info, self.db, data)
                if result:
                    self.json_return({
                        'code': 0,
                        'msg': '更改管理员信息成功'
                    })
                else:
                    self.json_return({
                        'code': 9901,
                        'error': '更改管理员信息失败'
                    })
            else:
                return False
        else:
            if isinstance(arg, int):
                pass
            else:
                return False
