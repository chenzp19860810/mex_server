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
import logging
import requests
from config.config import QINIU
from .sdk import Auth, put_file, etag, create_timestamp_anti_leech_url

logger = logging.getLogger(__name__)

'''
    七牛云帮助类
'''


class Qiniu:
    ### API 地址
    __api = 'http://api.qiniu.com'

    def __init__(self):
        self.__public_bucket_name = QINIU['public_bucket_name']
        self.__private_bucket_name = QINIU['private_bucket_name']
        self.__qiniu = Auth(QINIU['access_key'], QINIU['secret_key'])


    def put_image(self, image):
        """
        上传图片到七牛云空间
        :param image: 图片路径
        :return: 上传后的图片地址
        """
        # token 有效期 10 分钟
        base_url = self.__get_bucket_domain(self.__public_bucket_name)
        if base_url is None:
            logger.error('获取七牛云存储空间域名失败')
            raise RuntimeError('获取七牛云存储空间域名失败')

        if isinstance(image, str) and os.path.isfile(image):
            """通过文件路径上传
               如果传入的参数是文件路径
               则调用sdk上传 
            """
            file_hash = etag(image)
            file_save_name = file_hash.split('-')[0]
            token = self.__qiniu.upload_token(self.__public_bucket_name, file_save_name, 600)
            result, response = put_file(token, file_save_name, image)
            return base_url + '/' + result['key'] + QINIU['image_policy']
        else:
            raise TypeError('上传图片到七牛云 Error ')


    def put_backup(self, file_path):
        """
        上传备份文件
        :param file_path:
        :return:
        """
        file_dir, file_save_name = os.path.split(file_path)
        token = self.__qiniu.upload_token(self.__private_bucket_name, file_save_name, 600)
        result, response = put_file(token, file_save_name, file_path)
        assert result['key'] == file_save_name
        assert result['hash'] == etag(file_path)


    def get_backup_download_url(self, file_name):
        """
        获取备份文件的下载链接
        :param file_name:
        :return:
        """
        domain = self.__get_bucket_domain(self.__private_bucket_name)
        base_url = 'http:' + domain + '/' + file_name
        private_url = self.__qiniu.private_download_url(base_url)
        return private_url


    def __get_bucket_domain(self, bucket_name):
        """
        获取指定空间绑定的域名
        :param bucket_name: 空间名称
        :return:
        """
        con = '/v6/domain/list?tbl={0}'.format(bucket_name)
        url = self.__api + con
        accessToken = self.__qiniu.token_of_request(con)
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": "QBox " + accessToken,
            "Accept-Encoding": "gzip"
        }
        result = requests.get(url=url, headers=headers)
        if result.status_code == 200:
            result_list = list(result.json())
            if len(result_list) > 1:
                return_domain = result_list[1]
            else:
                return_domain = result_list[0]
            return '//' + return_domain
        else:
            return None
