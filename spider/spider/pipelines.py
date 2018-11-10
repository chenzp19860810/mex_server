# -*- coding: utf-8 -*-
from config.config import DEBUG
from config.conf.conf_db import engine_url
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .items import JaponxItem
from model.models import Movies
from extends.utils import str2time


class SpiderPipeline(object):
    """
        初始化数据库或redis连接
        重用
    """
    # 数据库连接池
    db_pool = None

    def __init__(self):
        if self.db_pool is None:
            engine = create_engine(engine_url, **dict(
                echo=DEBUG,  # 输出 sql
                echo_pool=DEBUG,
                pool_recycle=7200,  # 两个小时后回收连接池
                pool_size=30,
                max_overflow=20
            ))
            db_pool_session = sessionmaker(bind=engine)
            self.db_pool = db_pool_session()


    def process_item(self, item, spider):
        """
        Item 数据处理
        :param item: Item
        :param spider: 爬虫
        :return:
        """
        if isinstance(item, JaponxItem):
            data_count = self.db_pool.query(Movies).filter(Movies.category == 'japonx', Movies.name == item['name']).count()
            if data_count > 0:
                spider.crawler.engine.close_spider(spider, ' - 已经爬取过 - ')
            else:
                movie = Movies(
                    category='japonx',
                    name=item['name'],
                    title=item['title'],
                    cover=item['cover'],
                    description=item['description'],
                    play_url=item['play_url'],
                    created_at=str2time(item['created_at']),
                    female=item['female'],
                    seller=item['seller']
                )
                self.db_pool.add(movie)
                try:
                    self.db_pool.commit()
                except Exception as e:
                    print(e)
                    self.db_pool.rollback()
                return item

        else:
            return item
