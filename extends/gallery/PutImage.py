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
from .Catbox import Catbox
from .Weibo import Weibo
from extends.utils import image2base64

logger = logging.getLogger(__name__)

'''
    公共图库
    用于上传图片
    目前有微博、Catbox已经够用
    优先上传图片到微博
    微博上传失败 在上传到Catbox
'''

class PutImage:

    @staticmethod
    def upload(request_file):
        try:
            weibo_result = Weibo(image2base64(request_file)).upload()
            if weibo_result['state']:
                logger.info('上传图片到微博成功')
                return weibo_result
            else:
                ### 微博上传失败
                catbox_result = Catbox(request_file).upload()
                if catbox_result['state']:
                    return catbox_result
                else:
                    catbox_result['message'] = weibo_result['message'] + '  /  ' + catbox_result['message']
                    return catbox_result
        except Exception as e:
            logger.error('上传图片失败 {0}'.format(e))
            return {'state': False, 'message':'{0}'.format(e)}