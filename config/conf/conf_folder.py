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
from os import path, makedirs

"""
    全局绝对目录配置
"""
root = path.abspath(path.join(path.dirname(__file__), '../../'))
static_path = path.join(root, 'static')
template_path = path.join(root, 'views')
runtime_path = path.join(root, 'runtime')
cookies_path = path.join(runtime_path, 'cookies')
log_path = path.join(runtime_path, 'logs')
install_lock_path = path.join(runtime_path,'install.lock')


# 初始化目录
def init_folder():
    if not path.exists(static_path):
        makedirs(static_path, 0o755)
    if not path.exists(runtime_path):
        makedirs(runtime_path, 0o755)
    if not path.exists(cookies_path):
        makedirs(cookies_path, 0o755)
    if not path.exists(log_path):
        makedirs(log_path, 0o755)