# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class JaponxItem(Item):
    name = Field()  # 番号
    title = Field() # 标题
    cover = Field() # 封面
    play_url = Field() # 播放地址
    description = Field() # 简介
    female = Field() # 女优
    seller = Field() # 片商
    created_at = Field() # 时间