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
from tornado.web import url
from controller import (
    BaseHandler,
    UploadHnadler,
    ServerHandler,
    PostHandler,
    AttrbuHandler,
    BangumiHandler,
    LoginHandler,
    UserHandler,
    MovieHandler
)

### API 版本号
version = '1.5'

#################################################################################
######### API 路由映射
###     【GET       查询】      200     /{version}/{resources}                    // 返回资源对象的列表
###     【GET       查询】      200     /{version}/{resources}/{resource_id}      // 返回单个资源对象
###     【POST      添加】      201     /{version}/{resources}                    // 返回新生成的资源对象
###     【PUT       更新】      202     /{version}/{resources}/{resource_id}      // 返回完整的资源对象
###     【DELETE    删除】      200     /{version}/{resources}/{resource_id}      // 状态码 200
#################################################################################
url_api = [
    # 登录
    url(r'/v{}/(login|logout)'.format(version), LoginHandler.LoginHnadler, name="login"),
    # 极验接口
    url(r'/v{}/geetest/captchar'.format(version), LoginHandler.GetCaptchaHandler, name="geetest-register"),
    url(r'/v{}/geetest/validate'.format(version), LoginHandler.ValidateHandler, name="geetest-validate"),
    # 上传
    url(r'/v{}/music'.format(version), ServerHandler.ComponentsHandler, name='music'),
    url(r'/v{}/upload'.format(version), UploadHnadler.UploadHnadler, name='upload'),
    # 日志
    url(r'/v{}/logs'.format(version), ServerHandler.LogsHandler, name='logs'),
    # 分类 / 标签
    url(r'/v{}/tags'.format(version), AttrbuHandler.TagsHandler, name='tags'),
    url(r'/v{}/tags/(.*)'.format(version), AttrbuHandler.TagsHandler),
    url(r'/v{}/category'.format(version), AttrbuHandler.CategoryHandler, name='category'),
    url(r'/v{}/category/(.*)'.format(version), AttrbuHandler.CategoryHandler),
    # 文章
    url(r'/v{}/article'.format(version), PostHandler.ArticleHandler, name='article'),
    url(r'/v{}/article/(\d+)'.format(version), PostHandler.ArticleHandler),
    url(r'/v{}/article/([a-zA-Z0-9]+)'.format(version), PostHandler.ArticleHandler),
    # 番组
    url(r'/v{}/bangumi'.format(version), BangumiHandler.BangumiHandler, name='bangumi'),
    url(r'/v{}/bangumi/(\d+)'.format(version), BangumiHandler.BangumiHandler),
    # 菜单
    url(r'/v{}/menus'.format(version), ServerHandler.MenusHandler, name='menus'),
    url(r'/v{}/menus/(\d+)'.format(version), ServerHandler.MenusHandler),
    # 链接
    url(r'/v{}/links'.format(version), ServerHandler.LinksHnadler, name='links'),
    url(r'/v{}/links/(\d+)'.format(version), ServerHandler.LinksHnadler),
    # 用户
    url(r'/v{}/user'.format(version), UserHandler.UserHandler, name='user'),
    url(r'/v{}/user/(\d+)'.format(version), UserHandler.UserHandler),
    url(r'/v{}/user/(resetPass|info|\d+)'.format(version), UserHandler.UserHandler),
    url(r'/v{}/user/auth'.format(version), LoginHandler.LoginHnadler),
    # 配置
    url(r'/v{}/options'.format(version), ServerHandler.OptionsHandler, name='options'),
    url(r'/v{}/options/(.*)'.format(version), ServerHandler.OptionsHandler),
    # Movie
    url(r'/v{}/movie'.format(version), MovieHandler.MovieHandler, name='movie'),
    # 404
    url(r'.*', BaseHandler)
]
#################################################################################
######### END
#################################################################################