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
from os import path
from ..http import Http
from extends.utils import file_put_contents, file_get_contents
from config.conf.conf_folder import cookies_path

class TuBase:

    def __init__(self):
        self.http = Http()

    ### 返回微博cookies
    def get_weibo_cookies(self):
        weibo_cookies_path = path.join(cookies_path, 'weibo_cookies.dat')
        if not path.isfile(weibo_cookies_path):
            file_put_contents(weibo_cookies_path, '')
        return file_get_contents(weibo_cookies_path)