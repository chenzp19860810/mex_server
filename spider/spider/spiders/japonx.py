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
from scrapy import Spider, Request, Selector
from ..items import JaponxItem
from config.conf.conf_folder import root
from extends.utils import file_get_contents

class Japonx(Spider):
    name = 'japonx'

    config = file_get_contents(root + "/config/spider.json")
    config = json.loads(config)
    host = config[name]['host']
    vod_ajax_api = config[name]['ajax_api']

    allowed_domains = [host]
    start_urls = [
        'https://'+ host +'/portal/index/search/new/1.html?new=1&page=1'
    ]

    """"""
    host_url = 'https://' + host
    next_page = None
    """"""

    def parse(self, response):
        ### 查找下一页
        next_link = response.xpath('//*[@id="contents"]/div[2]/ul/li[last()]/a').extract_first()
        if next_link is None:
            self.next_page = None
        else:
            next_selecter = Selector(text=next_link)
            self.next_page = self.host_url + next_selecter.xpath('//a/@href').extract_first()
        ### 查找下一页 END
        li_list = response.xpath('//*[@id="works"]//li').extract()

        for item in li_list:
            select = Selector(text=item)
            details_url = select.xpath('//a/@href').extract()[0]
            details_url = self.host_url + details_url
            yield Request(details_url,self.get_vod_content)


    def get_vod_content(self, response):
        item = JaponxItem()
        item['title'] = response.xpath('//div[@id="contents-inline"]/h1/text()').extract_first()
        item['cover'] = response.xpath('//img[@id="do_play_1"]/@src').extract_first()
        item['description'] = response.xpath('//div[@id="contents-inline"]/p/text()').extract_first()
        item['name'] = response.xpath('//div[@id="contents-inline"]/div[2]/dl/dd[1]/a/text()').extract_first()
        item['female'] = response.xpath('//div[@id="contents-inline"]/div[2]/dl/dd[3]/a/text()').extract_first()
        item['seller'] = response.xpath('//div[@id="contents-inline"]/div[2]/dl/dd[6]/a/text()').extract_first()
        item['created_at'] = response.xpath('//div[@id="contents-inline"]/div[2]/dl/dd[4]/a/text()').extract_first()
        vod_id = response.url.split('id/')[1].split('.')[0]
        vod_play_info_url = self.vod_ajax_api + vod_id
        item['play_url'] = vod_play_info_url

        # 获取下一页
        if self.next_page is not None:
            yield Request(url=self.next_page, callback=self.parse)

        yield item