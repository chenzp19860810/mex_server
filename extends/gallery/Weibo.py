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
import binascii
from .TuBase import TuBase

logger = logging.getLogger(__name__)

'''
    微博床图
    由于登录微博会产生验证码
    这里只用微博cookies进行上传
'''

class Weibo(TuBase):

    upload_api = 'http://picupload.service.weibo.com/interface/pic_upload.php?mime=image%2Fjpeg&data=base64&url=0' \
                   '&markpos=1&logo=&nick=0&marks=1&controller=miniblog'
    cookies = None

    def __init__(self, base64_image_data):
        super().__init__()
        self.request = self.http.getRequest()
        self.cookies = self.get_weibo_cookies()
        self.image = base64_image_data

    def upload(self):
        if not self.cookies:
            result = {
                'state': False,
                'message': "请填写微博登录 cookies"
            }
            return result

        headers = {
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/69.0.3497.92 Safari/537.36',
            'Cookie': self.cookies
        }

        up_file = {
            'b64_data': self.image
        }

        # 上传
        response = self.request.post(self.upload_api, headers=headers, data=up_file)
        if response.status_code == 200:
            result_data = response.text.strip().replace('\n', '').split('</script>')
            if result_data[1]:
                json_result = json.loads(result_data[1])['data']
                if json_result['count'] > 0:
                    image_pid = json_result['pics']['pic_1']['pid']
                    img_url = self.__getImageUrl(image_pid)
                    result = {
                        "state": True,
                        "url": img_url
                    }
                else:
                    logger.error("上传图片到微博失败 ~  返回信息 : {0}".format(json_result))
                    result = {
                        "state": False,
                        "message": "上传图片到微博失败 ~ "
                    }
            else:
                logger.error("上传图片到微博失败 ")
                result = {
                    "state": False,
                    "message": "上传图片到微博失败 ~ "
                }
        else:
            logger.error("上传图片到微博失败 ~  状态码 : {0}  返回信息 : {1}".format(response.status_code, response.text))
            result = {
                "state": False,
                "message": "上传图片到微博失败 ~ "
            }

        return result


    def __getImageUrl(self, image_pid):
        return 'https://ww{0}{1}.{2}'.format(
            str((binascii.crc32(bytes(image_pid, encoding="utf-8")) & 3) + 1),
            '.sinaimg.cn/large/{0}'.format(image_pid),
            'gif' if image_pid[21] == 'g' else 'jpg'
        )