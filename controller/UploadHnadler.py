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
import os
from config.config import DEBUG
from controller import BaseHandler
from tornado.gen import coroutine
from extends.gallery import PutImage
from extends.qiniu import Qiniu
from config.conf.conf_folder import runtime_path

class UploadHnadler(BaseHandler):

    max_upload = 20  # 获取后台配置

    @coroutine
    def post(self, *args, **kwargs):
        """
            图片上传接口

            file    上传的文件
            options 上传文件选项 (后期添加文件裁剪等)

        :param args:
        :param kwargs:
        :return:
        """
        file_list = self.request.files.get('file', None)
        if file_list is None:
            self.error_return(400)
        else:
            file = file_list[0]
            upload_size = int(self.request.headers.get('Content-Length'))
            if upload_size / 1024 / 1024 > self.max_upload:
                self.json_return({
                    'code': 9901,
                    'error': '文件大小不能大于{0} ~'.format(self.max_upload)
                })
            else:
                file_type = file['content_type']
                if 'image' in file_type:
                    ### 调试模式用床图
                    ### 生产环境用七牛
                    ### 选择上传到 七牛云或者公共床图
                    if DEBUG:
                        result = yield self.upload_pubtu(file['body'])
                    else:
                        result = yield self.upload_qiniu(file)
                    if result['state']:
                        self.json_return({
                            'code':0,
                            'url':result['url']
                        })
                    else:
                        self.json_return({
                            'code': 9901,
                            'error': result['message']
                        })
                else:
                    self.error_return(400)


    @coroutine
    def upload_qiniu(self, file_data):
        """
        上传图片到七牛云
        :param file_data:  tornado 获取的文件对象
        :return:
        """
        tmp_f_path = os.path.join(runtime_path, 'tmp_cache.' + file_data['content_type'].split('/')[1])
        with open(tmp_f_path, 'wb') as tmp_f:
            tmp_f.write(file_data['body'])
        try:
            result = Qiniu().put_image(tmp_f_path)
            os.remove(tmp_f_path)
            if result:
                return {'state': True, 'url': result}
            else:
                return {'state': False, 'message': '分发文件到七牛云失败'}
        except Exception as e:
            return {'state': False, 'message': '分发文件到七牛云失败 {0}'.format(e)}

    @coroutine
    def upload_pubtu(self, file_data):
        """
        上传图片到公共床图
        :param file_data: tornado 获取的文件对象的 body  ===>  file['body']
        :return:
        """
        return PutImage.upload(file_data)
