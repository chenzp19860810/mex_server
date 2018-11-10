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
from controller import BaseHandler, auth_required
from model.pager import Pager
from model.models import to_dict
from service.LogService import LogService
from service.SettingService import MenusService
from service.FuncService import FuncService
from service.SettingService import OptionsService
from tornado import gen
import tornado.websocket


logger = logging.getLogger(__name__)


"""
    音乐API
"""
class ComponentsHandler(BaseHandler):


    @auth_required
    @gen.coroutine
    def get(self, *args, **kwargs):
        pass
        # result = musicApi.playlist.detail(161863791)
        # # if response.status_code == 200:
        # #     data = response.text
        # # else:
        # #     data = None
        # self.json_return({
        #     'code': 0,
        #     'data': result
        # })



"""
    后台社交配置
"""

class OptionsHandler(BaseHandler):

    @gen.coroutine
    def get(self, name=None, **kwargs):
        if name is None:
            self.error_return(400)
        else:
            result = yield self.async_do(OptionsService.query_options, self.db, name)
            self.json_return({
                'code':0,
                'data': result
            })


    @auth_required
    @gen.coroutine
    def put(self, name=None, **kwargs):
        if name is None:
            self.error_return(400)
        else:
            data = self.get_all_argument()
            result = yield self.async_do(OptionsService.update_options, self.db, name, data)
            if result:
                self.save_log("社交配置", "保存社交配置成功")
                self.json_return({
                    'code': 0,
                    'msg': '保存成功'
                })
            else:
                self.save_log("社交配置", "保存社交配置失败")
                self.json_return({
                    'code': 9901,
                    'error': '保存失败'
                })




"""
    后台友情链接操作
"""

class LinksHnadler(BaseHandler):


    @gen.coroutine
    def get(self, link_id=None, **kwargs):
        if link_id is None:
            pager = Pager(self)
            result = yield self.async_do(FuncService.query_link,self.db, pager=pager)
            self.json_return({
                'code':0,
                'data': to_dict(result)
            })
        else:
            result = yield self.async_do(FuncService.query_link, self.db, link_id=link_id)
            self.json_return({
                'code':0,
                'data': to_dict(result)
            })


    @auth_required
    @gen.coroutine
    def post(self, *args, **kwargs):
        data = self.get_all_argument()
        result = yield self.async_do(FuncService.add_link, self.db, data)
        if result:
            self.json_return({
                'code':0,
                'msg':'添加成功'
            })
        else:
            self.json_return({
                'code': 9901,
                'error': '添加失败'
            })

    @auth_required
    @gen.coroutine
    def put(self, link_id=None, **kwargs):
        data = self.get_all_argument()
        result = yield self.async_do(FuncService.update_link, self.db, link_id, data)
        if result:
            self.json_return({
                'code':0,
                'msg':'更新成功'
            })
        else:
            self.json_return({
                'code': 9901,
                'error': '更新失败'
            })


    @auth_required
    @gen.coroutine
    def delete(self, link_id=None, **kwargs):
        if link_id is None:
            self.error_return(400)
        else:
            result = yield self.async_do(FuncService.del_link, self.db, link_id)
            if result:
                self.json_return({
                    'code':0,
                    'msg':'删除成功'
                })
            else:
                self.json_return({
                    'code': 9901,
                    'error': '删除失败'
                })

"""
    后台菜单操作
"""
class MenusHandler(BaseHandler):

    @auth_required
    @gen.coroutine
    def get(self, menuId=None, **kwargs):
        if menuId is None:
            returnType = self.get_argument('return', 'tree')
            result = yield self.async_do(MenusService.query_menus, self.db, None, returnType)
            self.json_return({
                'code':0,
                'data': result
            })
        else:
            result = yield self.async_do(MenusService.query_menus, self.db, menuId)
            self.json_return({
                'code': 0,
                'data': to_dict(result)
            })


    @auth_required
    @gen.coroutine
    def post(self, *args, **kwargs):
        data = self.get_all_argument()
        result = yield self.async_do(MenusService.add_menus, self.db, data)
        if result:
            self.json_return({
                'code':0,
                'msg': '添加成功'
            })
        else:
            self.json_return({
                'code': 9901,
                'error':'添加失败'
            })



    @auth_required
    @gen.coroutine
    def put(self, menuId=None, **kwargs):
        if menuId is None:
            self.error_return(400)
        else:
            data = self.get_all_argument()
            result = self.async_do(MenusService.update_menus, self.db, menuId, data)
            if result:
                self.json_return({
                    'code': 0,
                    'msg': '更新成功'
                })
            else:
                self.json_return({
                    'code': 9901,
                    'error': '更新失败'
                })


    @auth_required
    @gen.coroutine
    def delete(self, menuId=None, **kwargs):
        if menuId is None:
            self.error_return(400)
        else:
            result = yield self.async_do(MenusService.del_menus, self.db, menuId)
            if result:
                self.json_return({
                    'code': 0,
                    'msg': '删除成功'
                })
            else:
                self.json_return({
                    'code': 9901,
                    'error': '删除失败'
                })



"""
    日志操作
"""
class LogsHandler(BaseHandler):

    @auth_required
    @gen.coroutine
    def get(self, *args, **kwargs):
        """
        查询日志  自动分页
        :param args:
        :param kwargs:
        :return:
        """
        pager = Pager(self)
        logList = yield self.async_do(LogService.log_list, self.db, pager)
        self.json_return({
            'code':0,
            'data': logList
        })

    @auth_required
    @gen.coroutine
    def delete(self, *args, **kwargs):
        """
        清空所有日志
        :param args:
        :param kwargs:
        :return:
        """
        result = yield self.async_do(LogService.clearLogs, self.db, self.client_ip)
        if result:
            self.json_return({
                'code':0
            })
        else:
            self.json_return({
                'code': 9904,
                'error': '出现错误'
            })


"""
    WebSocket 消息服务
"""
class MessageHandler(tornado.websocket.WebSocketHandler):

    user_list = set()

    ### 建立连接
    def open(self, *args, **kwargs):
        logger.info('开启websocket服务')
        ### 初始化
        self.user_list.add(self)

    #### 获取消息
    def on_message(self, message):
        logger.info('接收到客户端发来的消息')

    ### 关闭连接
    def on_close(self):
        logger.info('关闭websocket')
        ### 移除当前用户
        self.user_list.remove(self)

    #### 允许跨域
    def check_origin(self, origin):
        return True