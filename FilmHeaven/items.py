# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FilmheavenItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # 一级界面
    # 电影名字
    name = scrapy.Field()
    # 日期
    date = scrapy.Field()

    # 海报
    haibao = scrapy.Field()
    # 电影信息
    info = scrapy.Field()
    # 种子地址
    zhongzi = scrapy.Field()
