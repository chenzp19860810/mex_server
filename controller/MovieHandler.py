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
import re
import json
import logging
from . import BaseHandler, auth_required
from tornado import gen
from config.conf.conf_folder import root
from extends.http import Http
from extends.utils import file_get_contents
from model.pager import Pager
from service.MovieService import MovieService

logger = logging.getLogger(__name__)


class MovieHandler(BaseHandler):

    play_api = None
    ajax_api = None


    def __init__(self, application, request, **kwargs):
        super().__init__(application, request, **kwargs)

        config = file_get_contents(root + "/config/spider.json")
        config = json.loads(config)
        self.ajax_api = config['japonx']['ajax_api']
        self.play_api = config['japonx']['play_api']


    @auth_required
    @gen.coroutine
    def get(self, *args, **kwargs):
        """
        获取列表
        :param args:
        :param kwargs:
        :return:
        """
        pager = Pager(self)
        result = yield self.async_do(MovieService.movie_list, self.db, pager)
        self.json_return({
            'code': 0,
            'data': self.to_dict(result)
        })



    @auth_required
    @gen.coroutine
    def post(self, *args, **kwargs):
        data = self.get_all_argument()
        vid = data['vid'].strip() if 'vid' in data.keys() else None
        if vid is None:
            self.error_return(400)
        else:
            play_url = yield self.getM3u8Url(vid)
            if play_url is None:
                self.json_return({
                    'code': 1,
                    'error': '获取m3u8链接失败 ~'
                })
            else:
                self.json_return({
                    'code': 0,
                    'data': play_url
                })


    @gen.coroutine
    def getM3u8Url(self, id):
        """
        获取m3u8地址
        根据 ajax_api 返回的加密js解密出 m3u8 地址
        :param url:
        :return:
        """
        url = str(self.ajax_api) + str(id)
        html = Http().download_html(url=url)
        if html is None:
            return None
        else:
            result = html.strip()
            result = result.split('|url|')[1]
            html = result.split('\'.split')[0]
            key = [key for key in re.findall(r'^|([a-z0-9]{32})|', html, re.S) if key != '' and len(key) > 0]
            key = key[0] if len(key) > 0 else None
            md5 = [md5 for md5 in re.findall(r'^|([a-zA-Z0-9_]{22})|', html, re.S) if md5 != '' and len(md5) > 0]
            md5 = md5[1] if len(md5) > 1 else None
            expires = [expires for expires in re.findall(r'^|([0-9]{10})|', html, re.S) if expires != '' and len(expires) > 0]
            expires = expires[0] if len(expires) > 0 else None
            return_url = self.play_api.format(key, md5, expires)
            logger.info(" - movie - API : {0}".format(return_url))
            logger.info(key)
            logger.info(md5)
            logger.info(expires)
            logger.info(' - movie - END')
            return return_url