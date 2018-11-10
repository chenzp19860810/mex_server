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
import socket
import requests
import logging
from config.conf.conf_folder import root
from requests.adapters import HTTPAdapter

socket.setdefaulttimeout(30)
Request = requests.session()
logger = logging.getLogger(__name__)

'''
    封装 http 请求
'''


class Http:
    request = None

    header = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 '
                      'Safari/537.36',
        'Connection': 'keep-alive',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }

    def __init__(self):
        self.request = Request
        self.request.mount('http://', HTTPAdapter(max_retries=2))
        self.request.mount('https://', HTTPAdapter(max_retries=2))

    def getRequest(self):
        """
        获取Request对象
        :return:
        """
        return self.request

    def download_html(self, url, header=None):
        """
        抓取网页
        :param url:
        :param header:
        :return:
        """
        if header is None:
            header = self.header

        try:
            result = self.request.get(url=url, headers=header, timeout=30)
            if result.status_code == 200:
                return result.text
            else:
                logger.log("获取源码失败 {0} {1}".format(result.status_code, url))
                return None
        except Exception as e:
            logger.log("获取源码失败 {0} ".format(e))
            return None

    def download_file(self, url, file_save_path):
        """
        下载文件
        :param url:
        :param file_save_path:
        :return:
        """
        if not os.path.isfile(file_save_path):
            try:
                result = self.request.get(url=url, headers=self.header)
                if result.status_code is 200:
                    with open(file_save_path, 'wb') as file:
                        file.write(result.content)
                    return file_save_path.replace(root, '').replace('\\', '/')
                else:
                    logger.error("下载文件出错 URL : {0}  |  状态码 : {1}".format(url, result.status_code))
                    return ""
            except Exception as e:
                logger.error("下载文件出错 URL : {0}  |  {1}".format(url, e))
                return ""
        else:
            return file_save_path.replace(root, '').replace('\\', '/')
