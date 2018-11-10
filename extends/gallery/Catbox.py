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
from .TuBase import TuBase

logger = logging.getLogger(__name__)

'''
    Catbox 文件托管
    https://catbox.moe
    微博床图上传失败时的补救措施
'''

class Catbox(TuBase):

    upload_api = 'https://catbox.moe/user/api.php'

    def __init__(self, image_file_data):
        super().__init__()
        self.request = self.http.getRequest()
        self.image = image_file_data

    def upload(self):
        data = {
            'reqtype':'fileupload',
            'userhash':''
        }
        up_file = {
            "fileToUpload": ("image.jpg", self.image, "image/jpeg")
        }
        response = self.request.post(url=self.upload_api, data=data, files=up_file)
        if response.status_code == 200:
            result = {
                'state':True,
                'url': response.text
            }
        else:
            result = {
                'state': False,
                'message': '上传图片到 Catbox 失败'
            }
        return result